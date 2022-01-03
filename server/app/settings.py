import os
from typing import List, Type
from pydantic import BaseSettings

basedir = os.path.abspath(os.path.dirname(__file__))
dbdir: str = os.path.join(basedir, 'database/')
TASK1_TABLE=os.path.join(dbdir, "task1_table.csv")
TASK2_TABLE=os.path.join(dbdir, "task2_table.csv")

class Settings(BaseSettings):
    CONFIG_NAME: str = "base"
    USE_MOCK_EQUIVALENCY: bool = False
    DEBUG: bool = False

class DevelopmentConfig(Settings):
    CONFIG_NAME: str = "dev"
    SECRET_KEY: str = os.getenv(
        "DEV_SECRET_KEY", "dev_secret"
    )
    DEBUG: bool = True
    TESTING: bool = False
    
class ProductionConfig(Settings):
    CONFIG_NAME: str = "prod"
    SECRET_KEY: str = os.getenv("PROD_SECRET_KEY", "prod_secret")
    DEBUG: bool = False
    TESTING: bool = False

class TestingConfig(Settings):
    CONFIG_NAME: str = "test"
    SECRET_KEY: str = os.getenv("TEST_SECRET_KEY", "Thanos did nothing wrong")
    DEBUG: bool = True
    TESTING: bool = True

def get_config(config):
    return config_by_name[config]

EXPORT_CONFIGS: List[Type[Settings]] = [
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig,
]
config_by_name = {cfg().CONFIG_NAME: cfg() for cfg in EXPORT_CONFIGS}
