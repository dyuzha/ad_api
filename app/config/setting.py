from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "User Management API"
    allowed_origins: list = ["*"]

    # class Config:
        # env_file = ".env"

settings = Settings()
