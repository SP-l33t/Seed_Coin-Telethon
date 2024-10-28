import asyncio
import re
import aiohttp
import sys
from random import uniform
from bot.utils import logger
from bot.config import settings

appUrl = "https://cf.seeddao.org/"
baseUrl = "https://elb.seeddao.org"
actualData = "https://raw.githubusercontent.com/vanhbakaa/Seed-App-Mine-Seed-BOT-Telegram/refs/heads/main/cgi"

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
}


async def get_main_js_format(base_url):
    async with aiohttp.request(url=base_url, method="GET", headers=headers) as response:
        response.raise_for_status()
        try:
            content = await response.text()
            matches = re.findall(r'src="(/.*?\.js)"', content)
            return sorted(set(matches), key=len, reverse=True) if matches else None
        except Exception as e:
            logger.warning(f"Error fetching the base URL: {e}")
            return None


async def get_base_api(url):
    async with aiohttp.request(url=url, method="GET", headers=headers) as response:
        response.raise_for_status()
        try:
            logger.info("Checking for changes in api...")
            content = await response.text()
            match = re.search(r'baseURL:\s*"(.*?)"', content)

            if match:
                return match.group(1)
            else:
                logger.info(f"Could not find 'baseUrl' in {url}.")
                return None
        except Exception as e:
            logger.warning(f"Error fetching the JS file: {e}")
            return None


async def check_base_url():
    main_js_formats = await get_main_js_format(appUrl)
    if main_js_formats:
        async with aiohttp.request(url=actualData, method="GET", headers=headers) as response:
            js_ver = (await response.text()).strip()
        for js in main_js_formats:
            if js_ver in js:
                logger.success(f"No change in js file: <green>{js_ver}</green>")
                return True
        return False
    else:
        logger.info("Could not find any main.js format. Dumping page content for inspection:")
        try:
            async with aiohttp.request(url=appUrl, method="GET", headers=headers) as response:
                print((await response.text())[:1000])  # Print first 1000 characters of the page
                return False
        except Exception as e:
            logger.warning(f"Error fetching the base URL for content dump: {e}")
            return False


async def check_bot_update_loop(start_delay: 0):
    await asyncio.sleep(start_delay)
    while settings.TRACK_BOT_UPDATES:
        if not(await check_base_url()):
            sys.exit("Detected Bot updates. Contact me to check if it's safe to continue: https://t.me/SP_l33t")
        await asyncio.sleep(uniform(1500, 2000))
