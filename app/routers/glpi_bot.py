import logging
from config.ldap_config import ldap_config
from fastapi import APIRouter
from core.models import UserGetion
from services.ldap_service import LDAPService
from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)
router = APIRouter(prefix="", tags=["glpi_bot"])


@router.post("/get_user/mail")
def get_user_mail(user: UserGetion):
    """Возвращает запись mail пользователя по логину"""
    try:
        logger.debug(f"Received request for user: {user.model_dump()}")
        with LDAPService(ldap_config) as ldap_conn:
            user_data = ldap_conn.get_user_info(user, "mail")

            if not user_data:
                return JSONResponse(
                    status_code=404,
                    content={"detal": "User not found in Active Directory"}
                )

            return { "status": "success", "data": user_data }

    except Exception as e:
        logger.error(f"API error: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail":"Internal server error"}
        )


@router.get("/test/get_user")
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
