import logging
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


logger = logging.getLogger(__name__)


class LDAPConfig(BaseSettings):
    """
    Конфигурация LDAP, загружаемая из .env файла.
    Все чувствительные данные хранятся как SecretStr.
    """
    # Учётные данные администратора
    LDAP_ADMIN_USER: SecretStr
    LDAP_ADMIN_PASSWORD: SecretStr
    LDAP_SERVER_URL: str

    # TLS/SSL настройки (опционально)
    # use_ssl: bool = Field(False, env="LDAP_USE_SSL")
    # ca_cert_path: Optional[Path] = Field(None, env="LDAP_CA_CERT_PATH")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8"
        # secrets_dir = "/run/secrets"  # Для Docker Secrets
    )

    def get_admin_password(self) -> str:
        """Безопасное извлечение учётных данных"""
        return self.LDAP_ADMIN_PASSWORD.get_secret_value()
        # return self.LDAP_ADMIN_PASSWORD

    def get_admin_login(self) -> str:
        """Безопасное извлечение учётных данных"""
        return self.LDAP_ADMIN_USER.get_secret_value()
        # return self.LDAP_ADMIN_USER


# Создаём инстанс конфига (можно импортировать из других модулей)
try:
    ldap_config = LDAPConfig()
except Exception as e:
    logger.error(f"Ошибка загрузки конфига LDAP: {e}")
    raise
