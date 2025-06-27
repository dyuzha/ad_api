from pydantic import SecretStr
from .base import CommonBaseSettings

class LDAPConfig(CommonBaseSettings):
    LDAP_ADMIN_USER: SecretStr
    LDAP_ADMIN_PASSWORD: SecretStr
    LDAP_SERVER_URL: str

    # TLS/SSL настройки (опционально)
    # use_ssl: bool = Field(False, env="LDAP_USE_SSL")
    # ca_cert_path: Optional[Path] = Field(None, env="LDAP_CA_CERT_PATH")

    def get_admin_login(self) -> str:
        return self.LDAP_ADMIN_USER.get_secret_value()

    def get_admin_password(self) -> str:
        return self.LDAP_ADMIN_PASSWORD.get_secret_value()
