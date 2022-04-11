from dataclasses import dataclass
from os import path, environ

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


@dataclass
class Config:
    """
    Basic Configuration
    """
    BASE_DIR: str = base_dir
    DEBUG: bool = False
    TEST_MODE: bool = False


@dataclass
class LocalConfig(Config):
    DEBUG: bool = True
    TEST_MODE: bool = True


@dataclass
class ProdConfig(Config):
    DEBUG: bool = False
    TEST_MODE: bool = False


@dataclass
class TestConfig(Config):
    DEBUG: bool = False
    TEST_MODE: bool = True


def conf():
    config = dict(prod=ProdConfig, local=LocalConfig, test=TestConfig)
    return config[environ.get("ATM_ENV", "local")]()

