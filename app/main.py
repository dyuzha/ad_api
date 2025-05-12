import logging
from config.setting import settings
from core.logging import setup_logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import glpi_bot, user_manager


# Инициализация логирования
setup_logging()
logger = logging.getLogger(__name__)
logger.info("Application started")


app = FastAPI(title=settings.app_name)


# Разрешение запросов
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["POST"],
    )


#  Загрузка роутеров
app.include_router(glpi_bot.router)
# app.include_router(user_manager.router)
