> [!WARNING]
> ⚠️ I do my best to avoid detection of bots, but using bots is forbidden in all airdrops. i cannot guarantee that you will not be detected as a bot. Use at your own risk. I am not responsible for any consequences of using this software.


## Recommendation before use

# 🔥🔥 Use PYTHON 3.10 🔥🔥

## Features  
|                 Feature                 | Supported |
|:---------------------------------------:|:---------:|
|             Multithreading              |     ✅     |
|        Proxy binding to session         |     ✅     |
|              Auto-farming               |     ✅     |
|               Auto-tasks                |     ✅     |
|              Auto-upgrade               |     ✅     |
|              Auto-check-in              |     ✅     |
|                Auto-hunt                |     ✅     |
|                Auto-spin                |     ✅     |
|               Auto-fusion               |     ✅     |
|             Auto-sell worms             |     ✅     |
| Supports telethon AND pyrogram .session |     ✅     |

_Script searches for session files in the following folders:_
* /sessions
* /sessions/pyrogram
* /session/telethon


## [Settings](https://github.com/SP-l33t/Seed_Coin-Telethon/tree/main/.env-example)

# Use default setting for best performance !
|               Settings                |                                                                                                                  Description                                                                                                                  |
|:-------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|         **API_ID / API_HASH**         |                                                                                  Platform data from which to run the Telegram session (by default - android)                                                                                  |
|        **GLOBAL_CONFIG_PATH**         | Specifies the global path for accounts_config, proxies, sessions. <br/>Specify an absolute path or use an environment variable (default environment variable: **TG_FARM**) <br/>If no environment variable exists, uses the script directory. |
|             **FIX_CERT**              |                                                                                           Try to fix  SSLCertVerificationError ( True / **False** )                                                                                           |
|       **AUTO_UPGRADE_STORAGE**        |                                                                                                   Auto upgrade storage  (by default - True)                                                                                                   |
|        **AUTO_UPGRADE_MINING**        |                                                                                                 Auto upgrade mining speed (by default - True)                                                                                                 |
|         **AUTO_UPGRADE_HOLY**         |                                                                                                     Auto upgrade holy (by default - True)                                                                                                     |
|             **AUTO_TASK**             |                                                                                                          Auto tasks (default - True)                                                                                                          |
|             **AUTO_SPIN**             |                                                                                                          Auto spin (default - True)                                                                                                           |
|          **SPIN_PER_ROUND**           |                                                                                                   Spin count each round (default - [5, 10])                                                                                                   |
|            **AUTO_FUSION**            |                                                                                                 Auto fusion eggs if possible (default - True)                                                                                                 |
|  **MAXIMUM_PRICE_TO_FUSION_COMMON**   |                                                                                                 Max price to fusion common egg (default - 30)                                                                                                 |
| **MAXIMUM_PRICE_TO_FUSION_UNCOMMON**  |                                                                                               Max price to fusion uncommon egg (default - 200)                                                                                                |
|   **MAXIMUM_PRICE_TO_FUSION_RARE**    |                                                                                                 Max price to fusion rare egg (default - 800)                                                                                                  |
|   **MAXIMUM_PRICE_TO_FUSION_EPIC**    |                                                                                                 Max price to fusion epic egg (default - 3000)                                                                                                 |
| **MAXIMUM_PRICE_TO_FUSION_LEGENDARY** |                                                                                              Max price to fusion legendary egg (default - 20000)                                                                                              |
|          **AUTO_START_HUNT**          |                                                                                                       Auto start hunt (default - True)                                                                                                        |
|          **AUTO_SELL_WORMS**          |                                                                                                       Auto sell worms (default - True)                                                                                                        |
|         **QUANTITY_TO_KEEP**          |                                                       Quantity to keep worms check instruction [here](https://github.com/SP-l33t/Seed-App-Mine-Seed-BOT-Telegram/blob/main/setting.md)                                                        |
|              **REF_ID**               |                                                                                              Your referral id after startapp= (Your telegram ID)                                                                                              |
|    **RANDOM_SESSION_START_DELAY**     |                                                                                        Random delay at session start from 1 to set value (e.g. **30**)                                                                                        |
|        **SESSIONS_PER_PROXY**         |                                                                                            Amount of sessions, that can share same proxy ( **1** )                                                                                            |
|        **USE_PROXY_FROM_FILE**        |                                                                                Whether to use a proxy from the bot/config/proxies.txt file (**True** / False)                                                                                 |
|       **DISABLE_PROXY_REPLACE**       |                                                                      Disable automatic checking and replacement of non-working proxies before startup (True / **False**)                                                                      |
|           **DEVICE_PARAMS**           |                                                                          Enter device settings to make the telegram session look more realistic  (True / **False**)                                                                           |
|           **DEBUG_LOGGING**           |                                                                                     Whether to log error's tracebacks to /logs folder (True / **False**)                                                                                      |

## Quick Start 📚

To fast install libraries and run bot - open run.bat on Windows or run.sh on Linux

## Prerequisites
Before you begin, make sure you have the following installed:
- [Python](https://www.python.org/downloads/) **version 3.10**

## Obtaining API Keys
1. Go to my.telegram.org and log in using your phone number.
2. Select "API development tools" and fill out the form to register a new application.
3. Record the API_ID and API_HASH provided after registering your application in the .env file.


# Linux manual installation
```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp .env-example .env
nano .env  # Here you must specify your API_ID and API_HASH, the rest is taken by default
python3 main.py
```

You can also use arguments for quick start, for example:
```shell
~/Seed-App-Mine-Seed-BOT-Telegram >>> python3 main.py --action (1/2)
# Or
~/Seed-App-Mine-Seed-BOT-Telegram >>> python3 main.py -a (1/2)

# 1 - Run clicker
# 2 - Creates a session
```

# Windows manual installation
```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env-example .env
# Here you must specify your API_ID and API_HASH, the rest is taken by default
python main.py
```

You can also use arguments for quick start, for example:
```shell
~/Seed-App-Mine-Seed-BOT-Telegram >>> python main.py --action (1/2)
# Or
~/Seed-App-Mine-Seed-BOT-Telegram >>> python main.py -a (1/2)

# 1 - Run clicker
# 2 - Creates a session
```

### Contacts

For support or questions, you can contact me [![Static Badge](https://img.shields.io/badge/Telegram-Channel-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/airdrop_tool_vanh)
