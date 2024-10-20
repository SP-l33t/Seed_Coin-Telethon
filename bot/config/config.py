from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str
    GLOBAL_CONFIG_PATH: str = "TG_FARM"

    REF_ID: str = "525256526"

    AUTO_UPGRADE_STORAGE: bool = True
    AUTO_UPGRADE_MINING: bool = True
    AUTO_UPGRADE_HOLY: bool = True
    AUTO_CLEAR_TASKS: bool = True
    AUTO_START_HUNT: bool = True

    AUTO_SPIN: bool = True
    SPIN_PER_ROUND: list[int] = [5, 10]
    AUTO_FUSION: bool = True
    MAXIMUM_PRICE_TO_FUSION_COMMON: int = 30
    MAXIMUM_PRICE_TO_FUSION_UNCOMMON: int = 200
    MAXIMUM_PRICE_TO_FUSION_RARE: int = 800
    MAXIMUM_PRICE_TO_FUSION_EPIC: int = 3000
    MAXIMUM_PRICE_TO_FUSION_LEGENDARY: int = 20000

    AUTO_SELL_WORMS: bool = False
    QUANTITY_TO_KEEP: dict = {
        "common": {
            "quantity_to_keep": 2,
            "sale_price": 1
        },
        "uncommon": {
            "quantity_to_keep": 2,
            "sale_price": 0
        },
        "rare": {
            "quantity_to_keep": -1,
            "sale_price": 0
        },
        "epic": {
            "quantity_to_keep": -1,
            "sale_price": 0
        },
        "legendary": {
            "quantity_to_keep": -1,
            "sale_price": 0
        }
    }

    RANDOM_SESSION_START_DELAY: int = 30

    SESSIONS_PER_PROXY: int = 1
    USE_PROXY_FROM_FILE: bool = True
    DISABLE_PROXY_REPLACE: bool = False
    USE_PROXY_CHAIN: bool = False

    DEVICE_PARAMS: bool = False

    DEBUG_LOGGING: bool = False


settings = Settings()
