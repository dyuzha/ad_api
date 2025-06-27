import logging
from fastapi import HTTPException
from functools import wraps


logger = logging.getLogger(__name__)


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
