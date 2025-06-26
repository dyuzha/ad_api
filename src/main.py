import logging
from app.config.di import get_config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import glpi_bot, user_manager


config = get_config()


# Инициализация логирования
config.logger.setup()
logger = logging.getLogger(__name__)
logger.info("Application started")


app = FastAPI(title=config.common.app_name)


# Разрешение запросов
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.common.allowed_origins,
    allow_methods=["POST"],
    )


#  Загрузка роутеров
app.include_router(glpi_bot.router)
# app.include_router(user_manager.router)
