import logging
from ad_api.config import AppConfig
from fastapi import APIRouter, Depends, HTTPException
from ad_api.core.models import UserRegistration
from ad_api.services.ldap_service import LDAPService
from ad_api.config.di import get_config
from .depends import handle_ldap_errors


logger = logging.getLogger(__name__)
router = APIRouter(prefix="", tags=["user_manager"])


@router.post("/register")
@handle_ldap_errors
async def register_user(user: UserRegistration, app_config: AppConfig = Depends(get_config)):
    """Регистрирует нового пользователя"""
    with LDAPService(app_config.ldap) as ldap_conn:

        # Создаем пользователя
        success = ldap_conn.reg_user(user=user)
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to create user in LDAP"
            )

        # Изменяем мод пользователя
        success = ldap_conn.change_mode(user=user)
        if not success:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to change mode for {user.cn[:3]}"
            )

        # Добавляем пароль пользователю
        success = ldap_conn.password_update(user=user)
        if not success:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to change password for {user.cn[:3]}"
            )

    return {"status": "success", "login": user.sAMAccountName}


@router.get("/test_connection")
def get_test():
    """Проверяет соединение"""
    logger.info("Success connection")
    return {"message": "Success connection"}
