from .ldap import LDAPConfig
from .logging import LoggerConfigurator
from .base import CommonBaseSettings


class AppConfig:
    """Централизованный доступ к конфигурациям."""
    def __init__(self):
        self.common = CommonBaseSettings()
        self.ldap = LDAPConfig()
        self.logger = LoggerConfigurator()


__all__ = ["LDAPConfig", "AppConfig", "setup_logging", "CommonBaseSettings"]
