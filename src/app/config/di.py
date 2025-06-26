# src/config/di.py

from . import AppConfig

_config_instance = AppConfig()

def get_config() -> AppConfig:
    return _config_instance
