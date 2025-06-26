from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class CommonBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
            env_file="../.env" if os.getenv("ENV", "dev") == "dev" else None,
            env_file_encoding="utf-8",
            extra="ignore",
    )
    app_name: str = "AD API"
    allowed_origins: list = ["*"]
    # secrets_dir = "/run/secrets"  # Для Docker Secrets
