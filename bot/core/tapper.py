import aiohttp
import asyncio
import json
import pytz
import time
from urllib.parse import unquote, parse_qs
from aiocfscrape import CloudflareScraper
from aiohttp_proxy import ProxyConnector
from datetime import datetime, timezone
from better_proxy import Proxy
from random import uniform, randint, shuffle
from time import time

from bot.utils.universal_telegram_client import UniversalTelegramClient

from bot.config import settings
from bot.utils import logger, log_error, config_utils, CONFIG_PATH, first_run
from bot.exceptions import InvalidSession
from .headers import headers, get_sec_ch_ua

API_ENDPOINT = "https://alb.seeddao.org/api/v1"
# TODO Enable name task and refer
SKIP_TASK_CATEGORIES = ["telegram-boost",
                        "telegram-name-include",
                        "refer",
                        "collaboration",
                        "mint-bird-nft",
                        "ton-wallet-connect"]
VIDEO_ANSWERS = {
            "What is TON?": "Ton",
            "Coin vs Token": "Tokens",
            "What is Airdrop?": "Airdrop",
            "Hot vs Cold Wallet": "Wallet",
            "Crypto vs Blockchain": "Cryptocurrency",
            "Learn Blockchain in 3 mins": "Blockchain",
            "News affecting the BTC price": "BTCTOTHEMOON",
            "On-chain vs Off-chain #8": "TRANSACTION",
            "#10 Bullish and Bearish": "BULLRUN",
            "#13 SEED NFT Introduction": "BIRDIE"
        }


class Tapper:
    def __init__(self, tg_client: UniversalTelegramClient):
        self.tg_client = tg_client
        self.session_name = tg_client.session_name

        session_config = config_utils.get_session_config(self.session_name, CONFIG_PATH)

        if not all(key in session_config for key in ('api', 'user_agent')):
            logger.critical(self.log_message('CHECK accounts_config.json as it might be corrupted'))
            exit(-1)

        self.headers = headers
        user_agent = session_config.get('user_agent')
        self.headers['user-agent'] = user_agent
        self.headers.update(**get_sec_ch_ua(user_agent))

        self.proxy = session_config.get('proxy')
        if self.proxy:
            proxy = Proxy.from_str(self.proxy)
            self.tg_client.set_proxy(proxy)

        self.user_id = ''
        self.Total_Point_Earned = 0
        self.Total_Game_Played = 0
        self.worm_lvl = {"common": 1,
                         "uncommon": 2,
                         "rare": 3,
                         "epic": 4,
                         "legendary": 5}
        self.total_earned_from_sale = 0
        self.total_on_sale = 0
        self.worm_in_inv = {"common": 0, "uncommon": 0, "rare": 0, "epic": 0, "legendary": 0}
        self.worm_in_inv_copy = {"common": 0, "uncommon": 0, "rare": 0, "epic": 0, "legendary": 0}

        self.user_data = {}

        self._webview_data = None

    def log_message(self, message) -> str:
        return f"<ly>{self.session_name}</ly> | {message}"

    async def get_tg_web_data(self) -> str:
        webview_url = await self.tg_client.get_app_webview_url('seed_coin_bot', "app", "525256526")

        tg_web_data = unquote(string=webview_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        self.user_data = json.loads(parse_qs(tg_web_data).get('user', [''])[0])

        return tg_web_data

    async def check_proxy(self, http_client: CloudflareScraper) -> bool:
        proxy_conn = http_client.connector
        if proxy_conn and not hasattr(proxy_conn, '_proxy_host'):
            logger.info(self.log_message(f"Running Proxy-less"))
            return True
        try:
            response = await http_client.get(url='https://ifconfig.me/ip', timeout=aiohttp.ClientTimeout(15))
            logger.info(self.log_message(f"Proxy IP: {await response.text()}"))
            return True
        except Exception as error:
            proxy_url = f"{proxy_conn._proxy_type}://{proxy_conn._proxy_host}:{proxy_conn._proxy_port}"
            log_error(self.log_message(f"Proxy: {proxy_url} | Error: {type(error).__name__}"))
            return False

    async def setup_profile(self, http_client: CloudflareScraper) -> None:
        response = await http_client.post(url=f'{API_ENDPOINT}/profile')
        if response.status == 200:
            logger.info(self.log_message(f"<green>Set up account successfully!</green>"))

        else:
            logger.warning(self.log_message(f"Can't get account data <red>response status: {response.status}</red>"))

    async def hatch_egg(self, http_client: CloudflareScraper, egg_id):
        payload = {
            "egg_id": egg_id
        }
        res = await http_client.post(f'{API_ENDPOINT}/egg-hatch/complete', json=payload)
        if res.status == 200:
            json_data = await res.json()
            logger.success(self.log_message(f"Successfully hatched <lc>{json_data['data']['type']}</lc>!"))

    async def get_first_egg_and_hatch(self, http_client: CloudflareScraper):
        res = await http_client.post(f'{API_ENDPOINT}/give-first-egg')
        if res.status == 200:
            logger.success(self.log_message(f"Successfully <green>got first egg!</green>"))
            json_egg = await res.json()
            egg_id = str(json_egg['data']['id'])
            await self.hatch_egg(http_client, egg_id)

    async def fetch_profile(self, http_client: CloudflareScraper) -> None:
        response = await http_client.get(url=f'{API_ENDPOINT}/profile')
        if response.status == 200:
            response_json = await response.json()
            self.user_id = response_json['data']['id']
            logger.info(self.log_message(f"Got into seed app - Username: <green>{response_json['data']['name']}</green>"))
            if response_json['data']['give_first_egg'] is False:
                await self.get_first_egg_and_hatch(http_client)
            upgrade_levels = {}
            for upgrade in response_json['data']['upgrades']:
                upgrade_type = upgrade['upgrade_type']
                upgrade_level = upgrade['upgrade_level']
                if upgrade_type in upgrade_levels:
                    if upgrade_level > upgrade_levels[upgrade_type]:
                        upgrade_levels[upgrade_type] = upgrade_level
                else:
                    upgrade_levels[upgrade_type] = upgrade_level
            for upgrade_type, level in upgrade_levels.items():
                logger.info(self.log_message(f"<cyan>{upgrade_type.capitalize()} Level: {level + 1}</cyan>"))
        else:
            logger.warning(self.log_message(f"Can't get account data <red>response status: {response.status}</red>"))

    async def upgrade_storage(self, http_client: CloudflareScraper) -> None:
        response = await http_client.post(url=f'{API_ENDPOINT}/seed/storage-size/upgrade')
        if response.status == 200:
            logger.success(self.log_message(f"<yellow>Upgrade Storage Successfully</yellow>"))

    async def upgrade_mining(self, http_client: CloudflareScraper) -> None:
        response = await http_client.post(url=f'{API_ENDPOINT}/seed/mining-speed/upgrade')
        if response.status == 200:
            logger.success(self.log_message(f"<yellow>Upgrade Mining Successfully</yellow>"))

    async def upgrade_holy(self, http_client: CloudflareScraper) -> None:
        response = await http_client.post(url=f'{API_ENDPOINT}/upgrades/holy-water')
        if response.status == 200:
            logger.success(self.log_message(f"<yellow>Upgrade Holy Successfully</yellow>"))

    async def get_balance(self, http_client: CloudflareScraper):
        response = await http_client.get(url=f'{API_ENDPOINT}/profile/balance')
        if response.status in range(200, 300) and 'json' in response.content_type:
            balance_info = await response.json()
            logger.info(self.log_message(f"Balance: <lc>{balance_info.get('data', 0) / 1000000000}</lc>"))
            return balance_info.get('data', 0)
        else:
            logger.warning(self.log_message(f"<red>Balance: Error | {response.status}</red>"))

    async def perform_daily_checkin(self, http_client: CloudflareScraper):
        response = await http_client.post(f'{API_ENDPOINT}/login-bonuses')
        if response.status == 200:
            checkin_data = await response.json()
            day = checkin_data.get('data', {}).get('no', '')
            logger.success(self.log_message(f"Successfully <green>checked in | Day {day}</green>"))
        else:
            checkin_data = await response.json()
            if checkin_data.get('message') == 'already claimed for today':
                logger.info(self.log_message(f"Already checked in today"))
            else:
                logger.info(self.log_message(f"Failed | {checkin_data}"))

    async def fetch_worm_status(self, http_client: CloudflareScraper):
        response = await http_client.get(f'{API_ENDPOINT}/worms')
        if response.status == 200:
            worm_info = await response.json()
            next_refresh = worm_info['data'].get('next_worm')
            worm_caught = worm_info['data'].get('is_caught', False)
            if next_refresh:
                next_refresh_dt = datetime.fromisoformat(next_refresh[:-1] + '+00:00')
                now_utc = datetime.now(pytz.utc)
                time_difference_seconds = (next_refresh_dt - now_utc).total_seconds()
                hours = int(time_difference_seconds // 3600)
                minutes = int((time_difference_seconds % 3600) // 60)
                logger.info(self.log_message(
                    f"Next Worm in {hours} hours {minutes} minutes - Status: {'Caught' if worm_caught else 'Available'}"))
            else:
                logger.info(self.log_message(f"'next_worm' data not available."))
            return worm_info['data']
        else:
            logger.error(self.log_message(f"Error retrieving worm data."))
            return None

    async def capture_worm(self, http_client: CloudflareScraper):
        worm_info = await self.fetch_worm_status(http_client)
        if worm_info and not worm_info.get('is_caught', True):
            response = await http_client.post(f'{API_ENDPOINT}/worms/catch')
            if response.status == 200:
                logger.success(self.log_message(f"<green>Worm Captured Successfully</green>"))
            elif response.status == 400:
                logger.info(self.log_message(f"Already captured"))
            elif response.status == 404:
                logger.info(self.log_message(f"Worm not found"))
            else:
                logger.error(self.log_message(f"<red>Capture failed, status code: {response.status}</red>"))
        else:
            logger.info(self.log_message(f"Worm unavailable or already captured."))

    async def fetch_tasks(self, http_client: CloudflareScraper):
        response = await http_client.get(f'{API_ENDPOINT}/tasks/progresses')
        if 'json' in response.content_type:
            tasks = await response.json()
        else:
            return
        shuffle(tasks)
        for task in tasks['data']:
            if task.get('type', "") in SKIP_TASK_CATEGORIES:
                continue
            if not task['task_user'] or task['task_user']['completed'] is False:
                await self.mark_task_complete(task['id'], task['name'], task['type'], http_client)
                await asyncio.sleep(uniform(5, 10))

    async def mark_task_complete(self, task_id, task_name, type, http_client: CloudflareScraper):
        if type == "academy":
            if task_name not in VIDEO_ANSWERS:
                return
            payload = {"answer": VIDEO_ANSWERS[task_name]}
            response = await http_client.post(f'{API_ENDPOINT}/tasks/{task_id}', json=payload)
            if response.status == 200:
                logger.success(self.log_message(f"Task <lg>{task_name}</lg> marked complete."))
            else:
                logger.error(self.log_message(f"Failed to complete task {task_name}, status code: {response.status}"))
        else:
            response = await http_client.post(f'{API_ENDPOINT}/tasks/{task_id}')
            if response.status == 200:
                logger.success(self.log_message(f"Task <green>{task_name}</green> marked complete."))
            else:
                logger.error(self.log_message(f"Failed to complete task {task_name}, status code: {response.status}"))

    async def claim_hunt_reward(self, bird_id, http_client: CloudflareScraper):
        payload = {
            "bird_id": bird_id
        }
        response = await http_client.post(f'{API_ENDPOINT}/bird-hunt/complete', json=payload)
        if response.status == 200:
            response_data = await response.json()
            logger.success(self.log_message(
                f"Successfully claimed <green>{response_data['data']['seed_amount'] / (10 ** 9)}</green> "
                f"seed from hunt reward."))
        else:
            response_data = await response.json()
            logger.error(self.log_message(f"Failed to claim hunt reward, status code: {response.status}. {response_data}"))

    async def get_bird_info(self, http_client: CloudflareScraper):
        response = await http_client.get(f'{API_ENDPOINT}/bird/is-leader')
        if response.status == 200:
            response_data = await response.json()
            return response_data['data']
        else:
            response_data = await response.json()
            logger.info(self.log_message(f"Get bird data failed: {response_data}"))
            return None

    async def make_bird_happy(self, bird_id, http_client: CloudflareScraper):
        payload = {
            "bird_id": bird_id,
            "happiness_rate": 10000
        }
        response = await http_client.post(f'{API_ENDPOINT}/bird-happiness', json=payload)
        if response.status == 200:
            return True
        else:
            return False

    async def get_worm_data(self, http_client: CloudflareScraper):
        response = await http_client.get(f'{API_ENDPOINT}/worms/me-all')
        if response.status == 200:
            response_data = await response.json()
            return response_data['data']
        else:
            return None

    async def feed_bird(self, http_client: CloudflareScraper, bird_id, worm_ids):
        if not worm_ids:
            return
        payload = {
            "bird_id": bird_id,
            "worm_ids": worm_ids
        }
        response = await http_client.post(f'{API_ENDPOINT}/bird-feed', json=payload)
        if response.status == 200:
            logger.success(self.log_message(f"<green>Feed bird</green> successfully"))
        else:
            response_data = await response.json()
            logger.info(self.log_message(f"Failed to feed bird, response code:{response.status}. {response_data}"))
            return None

    async def start_hunt(self, bird_id, http_client: CloudflareScraper):
        payload = {
            "bird_id": bird_id,
            "task_level": 0
        }
        response = await http_client.post(f'{API_ENDPOINT}/bird-hunt/start', json=payload)
        if response.status == 200:
            logger.success(self.log_message(f"Successfully start <green>hunting</green>"))
        else:
            response_data = await response.json()
            logger.error(self.log_message(f"Start hunting failed..., response code: {response.status}. {response_data}"))

    async def get_worms(self, http_client: CloudflareScraper):
        worms = []
        first_page = await http_client.get(f'{API_ENDPOINT}/worms/me' + "?page=1")
        json_page = await first_page.json()

        for worm in json_page['data']['items']:
            worms.append(worm)
            if worm['on_market'] is False:
                self.worm_in_inv[worm['type']] += 1
        count = 0
        if json_page['data']['total'] % json_page['data']['page_size'] != 0:
            count = 1
        total_page = int(float(json_page['data']['total'] / json_page['data']['page_size'])) + count
        for page in range(2, total_page + 1):
            api_url = f'{API_ENDPOINT}/worms/me' + f"?page={page}"
            page_data = await http_client.get(api_url)
            json_page = await page_data.json()
            for worm in json_page['data']['items']:
                worms.append(worm)
                if worm['on_market'] is False:
                    self.worm_in_inv[worm['type']] += 1
            await asyncio.sleep(uniform(1, 2))
        return worms

    async def sell_worm(self, worm_id, price, worm_type, http_client: CloudflareScraper):
        payload = {
            "price": int(price),
            "worm_id": worm_id
        }
        response = await http_client.post(f'{API_ENDPOINT}/market-item/add', json=payload)
        if response.status == 200:
            self.total_on_sale += 1
            logger.success(self.log_message(
                f"Sell <green>{worm_type}</green> worm successfully, price: <green>{price / 1000000000}</green>"))
        else:
            response_data = await response.json()
            logger.info(self.log_message(f"Failed to sell {worm_type} worm, response code:{response.status}. {response_data}"))
            return None

    async def get_price(self, worm_type, http_client: CloudflareScraper):
        api = f'{API_ENDPOINT}v1/market/v2?market_type=worm&worm_type={worm_type}&sort_by_price=ASC&sort_by_updated_at=&page=1'
        response = await http_client.get(api)
        if response.status == 200:
            json_r = await response.json()
            return json_r['data']['items'][0]['price_gross']
        else:
            return 0

    async def get_sale_data(self, http_client: CloudflareScraper):
        api = f'{API_ENDPOINT}/history-log-market/me?market_type=worm&page=1&history_type=sell'
        response = await http_client.get(api)
        json_data = await response.json()
        worm_on_sale = {"common": 0, "uncommon": 0, "rare": 0, "epic": 0, "legendary": 0}
        for worm in json_data['data']['items']:
            if worm['status'] == "on-sale":
                worm_on_sale[worm['worm_type']] += 1
            elif worm['status'] == "bought":
                self.total_earned_from_sale += worm['price_net'] / 1000000000
        count = 0
        if json_data['data']['total'] % json_data['data']['page_size'] != 0:
            count = 1
        total_page = int(float(json_data['data']['total'] / json_data['data']['page_size'])) + count
        for page in range(2, total_page + 1):
            response = await http_client.get(
                f"{API_ENDPOINT}/history-log-market/me?market_type=worm&page={page}&history_type=sell")
            json_data = await response.json()
            for worm in json_data['data']['items']:
                if worm['status'] == "on-sale":
                    worm_on_sale[worm['worm_type']] += 1
                elif worm['status'] == "bought":
                    self.total_earned_from_sale += worm['price_net'] / 1000000000

        return worm_on_sale

    async def check_new_user(self, http_client: CloudflareScraper):
        response = await http_client.get(f'{API_ENDPOINT}/profile2')
        if response.status == 200:
            data_ = await response.json()
            return data_['data']['bonus_claimed']

    def refresh_data(self):
        self.total_earned_from_sale = 0
        self.worm_in_inv = self.worm_in_inv_copy

    async def get_streak_rewards(self, http_client: CloudflareScraper):
        res = await http_client.get(f"{API_ENDPOINT}/streak-reward")
        if res.status == 200:
            data_ = await res.json()
            return data_['data']
        else:
            logger.warning(f"{self.session_name} | <yellow>Failed to get streak rewards</yellow>")
        return None

    async def claim_streak_rewards(self, http_client: CloudflareScraper):
        rewards = await self.get_streak_rewards(http_client)
        pl_rewards = []
        if rewards is None:
            return
        if len(rewards) == 0:
            logger.info(self.log_message(f"No ticket to claim."))
            return
        for reward in rewards:
            pl_rewards.append(reward['id'])

        payload = {
            "streak_reward_ids": pl_rewards
        }
        claim = await http_client.post(f"{API_ENDPOINT}/streak-reward", json=payload)
        if claim.status == 200:
            logger.success(f"{self.session_name} | <green>Successfully claim tickets!</green>")
        else:
            logger.warning(f"{self.session_name} | <yellow>Failed to claim ticket!</yellow>")

    async def get_tickets(self, http_client: CloudflareScraper):
        res = await http_client.get(f"{API_ENDPOINT}/spin-ticket")
        if res.status == 200:
            data = await res.json()
            return data['data']
        return None

    async def get_egg_pieces(self, http_client: CloudflareScraper):
        res = await http_client.get(f"{API_ENDPOINT}/egg-piece")
        if res.status == 200:
            data = await res.json()
            return data['data']
        return None

    async def get_fusion_fee(self, type, http_client: CloudflareScraper):
        res = await http_client.get(f"{API_ENDPOINT}/fusion-seed-fee?type={type}")
        if res.status == 200:
            data = await res.json()
            return data['data']
        return None

    async def spin(self, ticketId, http_client: CloudflareScraper):
        payload = {
            "ticket_id": ticketId
        }

        res = await http_client.post(f"{API_ENDPOINT}/spin-reward", json=payload)
        if res.status == 200:
            data = await res.json()
            logger.success(f"{self.session_name} | <green>Spinned successfully - Got <cyan>{data['data']['type']}</cyan> egg pieces!</green>")
        else:
            return

    async def fusion(self, egg_ids, egg_type, http_client: CloudflareScraper):
        payload = {
            "egg_piece_ids": egg_ids
        }

        res = await http_client.post(f"{API_ENDPOINT}/egg-piece-merge", json=payload)
        if res.status == 200:
            logger.success(f"{self.session_name} | <green>Successfully fusion a <cyan>{egg_type}</cyan> egg!</green>")
        else:
            return

    async def get_eggs_in_inventory(self, http_client: CloudflareScraper):
        response = await http_client.get(f"{API_ENDPOINT}/egg/me?page=1")
        if response.status in range(200, 300) and 'json' in response.content_type:
            response = await response.json()
            return response.get('data', {}).get('items', [])

    async def get_egg_info(self, http_client: CloudflareScraper, egg_id):
        response = await http_client.get(f"{API_ENDPOINT}/egg/{egg_id}")
        if response in range(200, 300) and 'json' in response.content_type:
            return (await response.json()).get('data', {})

    async def egg_transfer_fee(self, http_client: CloudflareScraper, egg_type):
        response = await http_client.get(f"{API_ENDPOINT}/transfer/egg/estimate-fee?egg_type={egg_type}")
        if response.status in range(200, 300) and 'json' in response.content_type:
            return (await response.json()).get('data')

    async def transfer_egg(self, http_client: CloudflareScraper, egg_id, max_fee):
        balance = await self.get_balance(http_client)
        if settings.TRANSFER_EGGS == self.user_data.get('id'):
            return 'self'
        elif not settings.TRANSFER_EGGS or balance < max_fee:
            return False
        payload = {"telegram_id": settings.TRANSFER_EGGS, "egg_id": egg_id, "max_fee": max_fee}
        response = await http_client.post(f"{API_ENDPOINT}/transfer/egg", json=payload)
        if response.status in range(200, 300) and 'json' in response.content_type:
            response = await response.json()
            return bool(response.get('data', {}).get('received_by', ""))

    async def transfer_all_eggs(self, http_client: CloudflareScraper):
        eggs = await self.get_eggs_in_inventory(http_client)
        for egg in eggs:
            if egg.get('id') and egg.get('type') and egg.get('status', "") == "in-inventory":
                await self.get_egg_info(http_client, egg.get('id'))
                fee = await self.egg_transfer_fee(http_client, egg.get('type'))
                egg_transfer = await self.transfer_egg(http_client, egg.get('id'), fee)
                if egg_transfer == 'self':
                    return
                if egg_transfer:
                    logger.success(self.log_message(
                        f"Successfully transferred <lg>{egg.get('type')}</lg> egg to <lg>{settings.TRANSFER_EGGS}</lg>"))
                else:
                    logger.warning(self.log_message(
                        f"Failed to transferred <lg>{egg.get('type')}</lg> egg to <lg>{settings.TRANSFER_EGGS}</lg>"))
                await asyncio.sleep(uniform(5, 10))

    async def play_game(self, http_client: CloudflareScraper):
        egg_type = {
            "common": 0,
            "uncommon": 0,
            "rare": 0,
            "epic": 0,
            "legendary": 0
        }
        egg_pieces = await self.get_egg_pieces(http_client)
        if egg_pieces is None:
            return
        for piece in egg_pieces:
            egg_type[piece['type']] += 1

        info_ = f"Common: <lc>{egg_type['common']}</lc> | Uncommon: <lc>{egg_type['uncommon']}</lc> | " \
                f"Rare: <lc>{egg_type['rare']}</lc> | Epic: <lc>{egg_type['epic']}</lc> | " \
                f"Legendary: <lc>{egg_type['legendary']}</lc>"

        logger.info(self.log_message(f"Egg pieces: {info_}"))

        tickets = await self.get_tickets(http_client)
        if tickets is None:
            return

        logger.info(self.log_message(f"Total ticket: <cyan>{len(tickets)}</cyan>"))

        play = randint(settings.SPIN_PER_ROUND[0], settings.SPIN_PER_ROUND[1])

        for ticket in tickets:
            if play == 0:
                break
            play -= 1
            await self.spin(ticket['id'], http_client)
            await self.get_tickets(http_client)
            await self.get_egg_pieces(http_client)
            await asyncio.sleep(randint(2,5))

        if settings.AUTO_FUSION:
            egg_type = {
                "common": 0,
                "uncommon": 0,
                "rare": 0,
                "epic": 0,
                "legendary": 0
            }
            egg_pieces = await self.get_egg_pieces(http_client)
            if egg_pieces is None:
                return
            for piece in egg_pieces:
                egg_type[piece['type']] += 1

            if egg_type['common'] >= 5:
                fusion_fee = await self.get_fusion_fee('common', http_client)
                if fusion_fee is None:
                    return
                if fusion_fee/1000000000 <= settings.MAXIMUM_PRICE_TO_FUSION_COMMON:
                    pl_data = []
                    for piece in egg_pieces:
                        if len(pl_data) >= 5:
                            break
                        if piece['type'] == 'common':
                            pl_data.append(piece['id'])

                    await self.fusion(pl_data, 'common', http_client)

            if egg_type['uncommon'] >= 5:
                fusion_fee = await self.get_fusion_fee('uncommon', http_client)
                if fusion_fee is None:
                    return
                if fusion_fee/1000000000 <= settings.MAXIMUM_PRICE_TO_FUSION_UNCOMMON:
                    pl_data = []
                    for piece in egg_pieces:
                        if len(pl_data) >= 5:
                            break
                        if piece['type'] == 'uncommon':
                            pl_data.append(piece['id'])

                    await self.fusion(pl_data, 'uncommon', http_client)

            if egg_type['rare'] >= 5:
                fusion_fee = await self.get_fusion_fee('rare', http_client)
                if fusion_fee is None:
                    return
                if fusion_fee/1000000000 <= settings.MAXIMUM_PRICE_TO_FUSION_RARE:
                    pl_data = []
                    for piece in egg_pieces:
                        if len(pl_data) >= 5:
                            break
                        if piece['type'] == 'rare':
                            pl_data.append(piece['id'])

                    await self.fusion(pl_data, 'rare', http_client)

            if egg_type['epic'] >= 5:
                fusion_fee = await self.get_fusion_fee('epic', http_client)
                if fusion_fee is None:
                    return
                if fusion_fee/1000000000 <= settings.MAXIMUM_PRICE_TO_FUSION_EPIC:
                    pl_data = []
                    for piece in egg_pieces:
                        if len(pl_data) >= 5:
                            break
                        if piece['type'] == 'epic':
                            pl_data.append(piece['id'])

                    await self.fusion(pl_data, 'epic', http_client)

            if egg_type['legendary'] >= 5:
                fusion_fee = await self.get_fusion_fee('legendary', http_client)
                if fusion_fee is None:
                    return
                if fusion_fee/1000000000 <= settings.MAXIMUM_PRICE_TO_FUSION_LEGENDARY:
                    pl_data = []
                    for piece in egg_pieces:
                        if len(pl_data) >= 5:
                            break
                        if piece['type'] == 'legendary':
                            pl_data.append(piece['id'])

                    await self.fusion(pl_data, 'legendary', http_client)

    async def run(self) -> None:
        random_delay = uniform(1, settings.RANDOM_SESSION_START_DELAY)
        logger.info(self.log_message(f"Bot will start in <light-red>{int(random_delay)}s</light-red>"))
        await asyncio.sleep(delay=random_delay)

        access_token_created_time = 0
        tg_web_data = None

        proxy_conn = {'connector': ProxyConnector.from_url(self.proxy)} if self.proxy else {}
        async with CloudflareScraper(headers=self.headers, timeout=aiohttp.ClientTimeout(60), **proxy_conn) as http_client:
            while True:
                if not await self.check_proxy(http_client=http_client):
                    logger.warning(self.log_message('Failed to connect to proxy server. Sleep 5 minutes.'))
                    await asyncio.sleep(300)
                    continue

                token_live_time = randint(3500, 3600)
                try:
                    if time() - access_token_created_time >= token_live_time or not tg_web_data:
                        tg_web_data = await self.get_tg_web_data()

                        if not tg_web_data:
                            logger.warning(self.log_message('Failed to get webview URL'))
                            await asyncio.sleep(300)
                            continue

                        access_token_created_time = time()

                        http_client.headers["telegram-data"] = tg_web_data
                        await asyncio.sleep(delay=randint(10, 15))

                    not_new_user = await self.check_new_user(http_client)

                    if not_new_user is False:
                        logger.info(self.log_message(f"Setting up new account..."))
                        await self.setup_profile(http_client)

                    if self.tg_client.is_fist_run:
                        await first_run.append_recurring_session(self.session_name)

                    await self.fetch_profile(http_client)

                    if settings.AUTO_START_HUNT:
                        bird_data = await self.get_bird_info(http_client)
                        if bird_data is None:
                            logger.info(self.log_message(f"Can't get bird data..."))
                        elif bird_data['owner_id'] != self.user_id:
                            logger.warning(self.log_message(f"<yellow>Bird is not your: {bird_data}</yellow>"))
                        elif bird_data['status'] == "hunting":

                            try:
                                given_time = datetime.fromisoformat(bird_data['hunt_end_at'])
                                timestamp_naive = given_time.replace(tzinfo=None)
                            except:
                                import dateutil.parser
                                timestamp_naive = dateutil.parser.isoparse(bird_data['hunt_end_at'])
                            now = datetime.now(timezone.utc)

                            # If the parsed timestamp is naive, make it aware in UTC
                            if timestamp_naive.tzinfo is None:
                                timestamp_naive = timestamp_naive.replace(tzinfo=timezone.utc)

                            if now < timestamp_naive:
                                logger.info(self.log_message(f"Bird currently hunting..."))
                            else:
                                logger.info(self.log_message(f"<white>Hunt completed, claiming reward...</white>"))
                                await self.claim_hunt_reward(bird_data['id'], http_client)
                        else:
                            condition = True
                            if bird_data['happiness_level'] == 0:
                                logger.info(self.log_message(f"Bird is not happy, attemping to make bird happy..."))
                                check = await self.make_bird_happy(bird_data['id'], http_client)
                                if check:
                                    logger.success(self.log_message(f"Successfully <green>made bird happy!</green>"))
                                else:
                                    logger.info(self.log_message(f"Failed to make bird happy!"))
                                    condition = False
                            if bird_data['energy_level'] == 0:
                                logger.info(self.log_message(f"Bird is hungry, attemping to feed bird..."))
                                worms = await self.get_worm_data(http_client)
                                if worms is None:
                                    condition = False
                                    logger.info(self.log_message(f"Failed to fetch worm data"))
                                elif len(worms) == 0:
                                    logger.warning(self.log_message(f"You dont have any worm to feed bird!"))
                                    condition = False
                                else:
                                    try:
                                        energy = (bird_data['energy_max'] - bird_data['energy_level']) / 1000000000
                                    except:
                                        energy = 2
                                    wormss = []
                                    for worm in worms:
                                        if worm['type'] == "common" and worm['on_market'] is False:
                                            wormss.append(worm['id'])
                                            energy -= 2
                                            if energy <= 1:
                                                break
                                    if energy > 1:
                                        for worm in worms:
                                            if worm['type'] == "uncommon" and worm['on_market'] is False:
                                                wormss.append(worm['id'])
                                                energy -= 4
                                                if energy <= 1:
                                                    break
                                    await self.feed_bird(http_client, bird_data['id'], wormss)
                                    if energy > 1:
                                        condition = False

                            if condition:
                                await self.start_hunt(bird_data['id'], http_client)

                    if settings.AUTO_UPGRADE_STORAGE:
                        await self.upgrade_storage(http_client)
                        await asyncio.sleep(1)
                    if settings.AUTO_UPGRADE_MINING:
                        await self.upgrade_mining(http_client)
                        await asyncio.sleep(1)
                    if settings.AUTO_UPGRADE_HOLY:
                        await self.upgrade_holy(http_client)
                        await asyncio.sleep(1)

                    check_balance = await self.get_balance(http_client)
                    if check_balance:
                        response = await http_client.post(f'{API_ENDPOINT}/seed/claim')
                        if response.status == 200:
                            logger.success(self.log_message(f"<green> Claim successful </green>"))
                        elif response.status == 400:
                            logger.info(self.log_message(f"Not yet time to claim"))
                        else:
                            logger.error(self.log_message(
                                f"<red>An error occurred, status code: {response.status}</red>"))

                        await self.perform_daily_checkin(http_client)
                        await self.capture_worm(http_client)

                    if settings.TRANSFER_EGGS:
                        await self.transfer_all_eggs(http_client)

                    if settings.AUTO_SELL_WORMS:
                        logger.info(self.log_message("Fetching worms data to put it on sale..."))
                        worms = await self.get_worms(http_client)
                        worms_on_sell = await self.get_sale_data(http_client)
                        logger.info(self.log_message("Worms on sale now: "))
                        for worm in worms_on_sell:
                            logger.info(self.log_message(
                                f"Total <cyan>{worm}</cyan> on sale: <yellow>{worms_on_sell[worm]}</yellow>"))
                        logger.info(self.log_message(
                            f"Total earned from sale: <yellow>{self.total_earned_from_sale}</yellow>"))
                        for worm in worms:
                            if worm['on_market']:
                                continue
                            elif settings.QUANTITY_TO_KEEP[worm['type']]['quantity_to_keep'] == -1:
                                continue
                            elif settings.QUANTITY_TO_KEEP[worm['type']]['quantity_to_keep'] < \
                                    self.worm_in_inv[worm['type']]:
                                if settings.QUANTITY_TO_KEEP[worm['type']]['sale_price'] == 0:
                                    price_to_sell = await self.get_price(worm['type'], http_client)

                                else:
                                    price_to_sell = settings.QUANTITY_TO_KEEP[worm['type']]['sale_price'] * (10 ** 9)
                                await self.sell_worm(worm['id'], price_to_sell, worm['type'], http_client)
                                self.worm_in_inv[worm['type']] -= 1

                        self.refresh_data()
                    if settings.AUTO_CLEAR_TASKS:
                        await self.fetch_tasks(http_client)

                    if settings.AUTO_SPIN:
                        await self.claim_streak_rewards(http_client)
                        await asyncio.sleep(randint(1, 4))
                        await self.play_game(http_client)

                    delay_time = uniform(3500, 7200)
                    logger.info(self.log_message(f"Completed cycle, waiting {int(delay_time)} seconds..."))
                    await asyncio.sleep(delay_time)
                except InvalidSession as error:
                    raise error

                except Exception as error:
                    sleep_time = randint(60, 120)
                    log_error(self.log_message(f"Unknown error: {error}. Sleep {sleep_time} seconds"))
                    await asyncio.sleep(delay=sleep_time)


async def run_tapper(tg_client: UniversalTelegramClient):
    runner = Tapper(tg_client=tg_client)
    try:
        await runner.run()
    except InvalidSession as e:
        logger.error(runner.log_message(f"Invalid Session: {e}"))
