import logging
from core.logging import setup_logging
from services.ldap_service import LDAPService
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from core.models import UserRegistration, UserGetion
from config.setting import settings
from config.ldap_config import ldap_config
from functools import wraps


# Инициализация логирования
setup_logging()
logger = logging.getLogger(__name__)


app = FastAPI(title=settings.app_name)

def handle_ldap_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            raise HTTPException(status_code=400, detail=str())
        return result
    return wrapper

# Разрешение запросов
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["POST"],
    )

@app.post("/register")
@handle_ldap_errors
async def register_user(user: UserRegistration):
    """Регистрирует нового пользователя"""
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


@app.get("/test_connection")
def get_test():
    """Проверяет соединение"""
    logger.info("Success connection")
    return {"message": "Success connection"}


@app.post("/get_user_mail")
@handle_ldap_errors
def get_user_mail(user: UserGetion):
    with LDAPService(ldap_config) as ldap_conn:
        success = ldap_conn.get_user(user=user)
        if success is False:
            raise HTTPException(status_code=500, detail=f"Ошибка во время поиска пользователя: {user.sAMAccountName}")
        elif success is None:
            return {"status": "success", "mail":"None"}
        else:
            return {"status": "success", "mail":success.mail.value}


@app.get("/test/get_user")
@handle_ldap_errors
def get_test_user():
    try:
        with LDAPService(ldap_config) as ldap_conn:
            user_data = ldap_conn.get_test_user()

            if not user_data:
                return JSONResponse(
                    status_code=404,
                    content={"detal": "User not found in Active Directory"}
                )

            return { "status": "success", "data": user_data }

    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail":"Internal server error"}
        )
