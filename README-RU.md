[![Static Badge](https://img.shields.io/badge/Telegram-Channel-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/+jJhUfsfFCn4zZDk0)      [![Static Badge](https://img.shields.io/badge/Telegram-Bot%20Link-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/seed_coin_bot/app?startapp=525256526)



## Recommendation before use

# 🔥🔥 PYTHON version must be 3.10 🔥🔥

> 🇪🇳 README in english available [here](README)

## Функционал  
|               Функционал               | Поддерживается |
|:--------------------------------------:|:--------------:|
|            Многопоточность             |       ✅        | 
|        Привязка прокси к сессии        |       ✅        | 
| Использование вашей реферальной ссылки |       ✅        |
|               Авто фарм                |       ✅        |
|        Авто выполнение заданий         |       ✅        |
|             Авто улучшения             |       ✅        |
|               Авто охота               |       ✅        |
|               Авто спины               |       ✅        |
|            Авто скрещивание            |       ✅        |
|     Автоматическая продажа червей      |       ✅        |
|    Автоматичесие ежедневная стрики     |       ✅        |
| Поддержка telethon И pyrogram .session |       ✅        |

_Скрипт осуществляет поиск файлов сессий в следующих папках:_
* /sessions
* /sessions/pyrogram
* /session/telethon


## [Настройки](https://github.com/SP-l33t/Seed_Coin-Telethon/tree/main/.env-example)
|               Настройки               |                                                                                                                              Описание                                                                                                                               |
|:-------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|         **API_ID / API_HASH**         |                                                                                         Данные платформы, с которой будет запущена сессия Telegram (по умолчанию - android)                                                                                         |
|        **GLOBAL_CONFIG_PATH**         | Определяет глобальный путь для accounts_config, proxies, sessions. <br/>Укажите абсолютный путь или используйте переменную окружения (по умолчанию - переменная окружения: **TG_FARM**)<br/> Если переменной окружения не существует, использует директорию скрипта |
|             **FIX_CERT**              |                                                                                              Попытаться исправить ошибку SSLCertVerificationError ( True / **False** )                                                                                              |
|         **TRACK_BOT_UPDATES**         |                                                                         Отслеживать обновления бота и останавливать бота, если были обновления, для проверки изменений ( **True** /False )                                                                          |
|       **AUTO_UPGRADE_STORAGE**        |                                                                                                      Автоматическое обновление хранилища (по умолчанию - True)                                                                                                      |
|        **AUTO_UPGRADE_MINING**        |                                                                                                   Автоматическое повышение скорости добычи (по умолчанию - True)                                                                                                    |
|         **AUTO_UPGRADE_HOLY**         |                                                                                                   Автоматическое повышение уровня святости (по умолчанию - True)                                                                                                    |
|             **AUTO_TASK**             |                                                                                                       Автоматическое выполнение заданий (по умолчанию - True)                                                                                                       |
|             **AUTO_SPIN**             |                                                                                                             Автоматические spin'ы ( **True** / False )                                                                                                              |
|          **SPIN_PER_ROUND**           |                                                                                                              Количество спинов за круг ( **[5, 10]** )                                                                                                              |
|            **AUTO_FUSION**            |                                                                                                           Автоматическое вылупление яиц (default - True)                                                                                                            |
|  **MAXIMUM_PRICE_TO_FUSION_COMMON**   |                                                                                                     Максимальная цена за вылупление яиц: common (default - 30)                                                                                                      |
| **MAXIMUM_PRICE_TO_FUSION_UNCOMMON**  |                                                                                                    Максимальная цена за вылупление яиц:uncommon (default - 200)                                                                                                     |
|   **MAXIMUM_PRICE_TO_FUSION_RARE**    |                                                                                                      Максимальная цена за вылупление яиц:rare (default - 800)                                                                                                       |
|   **MAXIMUM_PRICE_TO_FUSION_EPIC**    |                                                                                                     Максимальная цена за вылупление яиц: epic (default - 3000)                                                                                                      |
| **MAXIMUM_PRICE_TO_FUSION_LEGENDARY** |                                                                                                  Максимальная цена за вылупление яиц: legendary (default - 20000)                                                                                                   |
|         **JOIN_GUILD_BY_ID**          |                                                                                Автоматически вступать в гильдию по ID из реф ссылки (пример "1b6983d3-d03c-4c1b-9ddd-2ab293dc893c")                                                                                 |
|          **AUTO_START_HUNT**          |                                                                                                          Автоматическое начало охоты (по умолчанию - True)                                                                                                          |
|          **AUTO_SELL_WORMS**          |                                                                                                         Автоматическая продажа червей (по умолчанию - True)                                                                                                         |
|         **QUANTITY_TO_KEEP**          |                                                           Количество для хранения инструкции по проверке червей [здесь](https://github.com/SP-l33t/Seed-App-Mine-Seed-BOT-Telegram/blob/main/setting.md)                                                            |
|              **REF_ID**               |                                                                                                  Ваш реферальный идентификатор после startapp= (Ваш ID в Telegram)                                                                                                  |
|    **RANDOM_SESSION_START_DELAY**     |                                                                                           Случайная задержка при запуске. От 1 до указанного значения (например, **30**)                                                                                            |
|        **SESSIONS_PER_PROXY**         |                                                                                            Количество сессий, которые могут использовать один и тот же прокси ( **1** )                                                                                             |
|        **USE_PROXY_FROM_FILE**        |                                                                                              Использовать ли прокси из файла bot/config/proxies.txt (**True** / False)                                                                                              |
|       **DISABLE_PROXY_REPLACE**       |                                                                                   Отключить автоматическую проверку и замену нерабочих прокси перед стартом ( True / **False** )                                                                                    |
|           **DEVICE_PARAMS**           |                                                                                 Введите настройки устройства, чтобы телеграмм-сессия выглядела более реалистично (True / **False**)                                                                                 |
|           **DEBUG_LOGGING**           |                                                                                               Включить логирование трейсбэков ошибок в папку /logs (True / **False**)                                                                                               |

## Быстрый старт 📚

Для быстрой установки и последующего запуска - запустите файл run.bat на Windows или run.sh на Линукс

## Предварительные условия
Прежде чем начать, убедитесь, что у вас установлено следующее:
- [Python](https://www.python.org/downloads/) **версии 3.10**

## Получение API ключей
1. Перейдите на сайт [my.telegram.org](https://my.telegram.org) и войдите в систему, используя свой номер телефона.
2. Выберите **"API development tools"** и заполните форму для регистрации нового приложения.
3. Запишите `API_ID` и `API_HASH` в файле `.env`, предоставленные после регистрации вашего приложения.

## Установка
Вы можете скачать [**Репозиторий**](https://github.com/SP-l33t/Seed_Coin-Telethon) клонированием на вашу систему и установкой необходимых зависимостей:
```shell
git clone https://github.com/GravelFire/MajorBot.git
cd MajorBot
```

Затем для автоматической установки введите:

Windows:
```shell
run.bat
```

Linux:
```shell
run.sh
```

# Linux ручная установка
```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp .env-example .env
nano .env  # Здесь вы обязательно должны указать ваши API_ID и API_HASH , остальное берется по умолчанию
python3 main.py
```

Также для быстрого запуска вы можете использовать аргументы, например:
```shell
~/MajorBot >>> python3 main.py --action (1/2)
# Or
~/MajorBot >>> python3 main.py -a (1/2)

# 1 - Запускает кликер
# 2 - Создает сессию
```


# Windows ручная установка
```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env-example .env
# Указываете ваши API_ID и API_HASH, остальное берется по умолчанию
python main.py
```

Также для быстрого запуска вы можете использовать аргументы, например:
```shell
~/MajorBot >>> python main.py --action (1/2)
# Или
~/MajorBot >>> python main.py -a (1/2)

# 1 - Запускает кликер
# 2 - Создает сессию
```
