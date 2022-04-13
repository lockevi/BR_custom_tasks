from dataclasses import dataclass
from os import path, environ


@dataclass
class Config:
    """
    Basic Configuration
    """
    DEBUG: bool = False
    TEST_MODE: bool = False


@dataclass
class LocalConfig(Config):
    """Configuration for local development"""
    DEBUG: bool = True
    TEST_MODE: bool = True


@dataclass
class ProdConfig(Config):
    """Configuration for production device"""
    DEBUG: bool = False
    TEST_MODE: bool = False


@dataclass
class TestConfig(Config):
    """Configuration for local testing"""
    DEBUG: bool = False
    TEST_MODE: bool = True


def conf() -> Config:
    config = dict(prod=ProdConfig, local=LocalConfig, test=TestConfig)
    return config[environ.get("ATM_ENV", "local")]()

