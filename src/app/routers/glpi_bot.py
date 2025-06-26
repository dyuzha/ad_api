import logging
from fastapi import APIRouter, Depends, HTTPException
from app.config import AppConfig
from app.config.di import get_config
from app.core.models import UserGetion
from app.services.ldap_service import LDAPService
from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)
router = APIRouter(prefix="", tags=["glpi_bot"])


@router.post("/get_user/mail")
def get_user_mail(user: UserGetion, app_config: AppConfig = Depends(get_config)):
    """Возвращает mail пользователя по логину"""
    try:
        logger.debug(f"Received request for user: {user.model_dump()}")

        with LDAPService(app_config.ldap) as ldap_conn:
            user_data = ldap_conn.get_user_info(user, "mail")

            if not user_data:
                raise HTTPException(
                    status_code=404,
                    detail="User not found in Active Directory"
                )

            response_data = {
                "status": "success",
                    "data": {
                        "mail": user_data["mail"],
                        "login": user.sAMAccountName
                    }
            }
            logger.debug(f"Returning response: {response_data}")
            return response_data

    except HTTPException:
        # Пробрасываем уже обработанные HTTP исключения
        raise

    except Exception as e:
        logger.error(f"Error API: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error") from e


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
