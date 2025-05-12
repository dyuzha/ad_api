import logging
from config.ldap_config import ldap_config
from fastapi import APIRouter, HTTPException
from core.models import UserRegistration
from services.ldap_service import LDAPService
from .depends import handle_ldap_errors


logger = logging.getLogger(__name__)
router = APIRouter(prefix="", tags=["user_manager"])


@router.post("/register")
@handle_ldap_errors
async def register_user(user: UserRegistration):
    """Регистрирует нового пользователя"""
    with LDAPService(ldap_config) as ldap_conn:

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
