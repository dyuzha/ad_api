import logging
from core.logging import setup_logging
from services.ldap_service import LDAPService
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.models import UserRegistration, UserEditor, UserToTrash
from config.setting import settings
from config.ldap_config import ldap_config

# Инициализация логирования
setup_logging()
logger = logging.getLogger(__name__)


app = FastAPI(title=settings.app_name)

# Разрешение запросов
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["POST"],
    )


@app.post("/register")
async def register_user(user: UserRegistration):
    """Регистрирует нового пользователя"""
    try:
        with LDAPService(ldap_config) as ldap_conn:
            # Создаем пользователя
            success = ldap_conn.reg_user(user=user)
            if not success:
                raise HTTPException(status_code=500, detail="Failed to create user in LDAP")

            # Изменяем мод пользователя
            success = ldap_conn.change_mode(user=user)
            if not success:
                raise HTTPException(status_code=500, detail=f"Failed to change mode for {user.cn[:3]}")

            # Добавляем пароль пользователю
            success = ldap_conn.password_update(user=user)
            if not success:
                raise HTTPException(status_code=500, detail=f"Failed to change password for {user.cn[:3]}")

        return {"status": "success", "login": user.sAMAccountName}

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/edit")
async def edit_user(user: UserEditor):
    """Изменяет существующего пользователя"""
    try:
        with LDAPService(ldap_config) as ldap_conn:

            # Добавляем пароль пользователю
            success = ldap_conn.password_update(user=user)
            if not success:
                raise HTTPException(status_code=500, detail=f"Failed to change password for {user.cn[:3]}")

        return {"status": "success", "login": user.sAMAccountName}

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/to_trash_user")
async def to_trash_user(user: UserToTrash):
    """Перемещает пользователя в корзину и очищает группы"""
    pass


@app.get("/test_connection")
def get_test():
    """Проверяет соединение"""
    logger.info("Success connection")
    return {"message": "Success connection"}
