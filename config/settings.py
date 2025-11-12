import os


class BaseConfig:
    DEBUG = False
    AUTO_SAVE_INTERVAL = int(os.getenv("AUTO_SAVE_INTERVAL", "600"))


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    AUTO_SAVE_INTERVAL = int(os.getenv("AUTO_SAVE_INTERVAL", "60"))


class ProductionConfig(BaseConfig):
    AUTO_SAVE_INTERVAL = int(os.getenv("AUTO_SAVE_INTERVAL", "600"))


def get_config(env):
    if env == "production":
        return ProductionConfig
    return DevelopmentConfig
