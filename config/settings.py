class BaseConfig:
    SECRET_KEY = "replace_me"
    DEBUG = False
    # Auto-save interval in seconds
    AUTO_SAVE_INTERVAL = 600


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DATABASE_URI = "sqlite:///dev.db"
    # Development uses more frequent auto-save for testing
    AUTO_SAVE_INTERVAL = 60


class ProductionConfig(BaseConfig):
    DATABASE_URI = "postgresql://user:password@db:5432/my_api"


def get_config(env):
    if env == "production":
        return ProductionConfig
    return DevelopmentConfig
