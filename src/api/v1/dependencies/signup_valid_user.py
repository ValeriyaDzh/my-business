import logging

from fastapi import Depends
from jose import JWTError

from src.middlware.auth import oauth2_scheme
from src.utils.auth import TokenService
from src.utils.exceptions import ForbiddenException

logger = logging.getLogger(__name__)


async def valid_user(
    token=Depends(oauth2_scheme),
    token_service: TokenService = Depends(TokenService),
) -> str:
    try:
        decoded_token = token_service.decode_jwt(token)
        email = decoded_token.get("email")
        logger.debug(f"User email check: {email}")
        if not email:
            raise ForbiddenException
        return email
    except JWTError as e:
        logger.error(f"Error decoding jwt token: {e}")
        raise ForbiddenException
