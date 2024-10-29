import logging
import random
from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt
from redis import Redis

from src.config import settings

logger = logging.getLogger(__name__)


class TokenService:

    cache: Redis = settings.cache.REDIS

    @staticmethod
    def generate_signup_token() -> None:
        return random.randint(1000, 9999)

    def save_signup_token(self, account: str, token: int, ttl: int = 300) -> None:
        self.cache.setex(account, ttl, token)

    def verify_signup_token(self, account: str, token: int) -> bool:
        saved_token = self.cache.get(account)
        logger.debug(f"{saved_token}")
        if saved_token and int(saved_token) == token:
            self.cache.delete(account)
            logger.debug(f"Email {account} has been verified")
            return True
        return False

    @staticmethod
    def decode_jwt(token: str | bytes) -> dict:
        decoded = jwt.decode(
            token=token,
            key=settings.jwt.SECRET_KEY.get_secret_value(),
            algorithms=settings.jwt.ALGORITHM,
        )
        return decoded

    def create_access_token(
        self,
        data: dict[str, Any],
        expires_delta: timedelta | None = None,
    ) -> str:
        logger.debug(f"Creating token...for data {data}")

        payload = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(
                minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES,
            )
        encoded_access_jwt = self._encode_jwt(payload, expire)
        logger.debug("Created")
        return encoded_access_jwt

    @staticmethod
    def _encode_jwt(data_dict: dict, expires_delta: timedelta) -> str:
        to_encode = data_dict.copy()
        to_encode.update({"exp": expires_delta})
        encoded = jwt.encode(
            claims=to_encode,
            key=settings.jwt.SECRET_KEY.get_secret_value(),
            algorithm=settings.jwt.ALGORITHM,
        )
        return encoded
