import logging
import random

from redis import Redis

from src.config import settings

logger = logging.getLogger(__name__)


class TokenService:

    cache: Redis = settings.cache.REDIS

    def generate_signup_token(self):
        return random.randint(1000, 9999)

    def save_signup_token(self, account: str, token: int, ttl: int = 300):
        self.cache.setex(account, ttl, token)

    def verify_signup_token(self, account: str, token: int) -> bool:
        saved_token = self.cache.get(account)
        logger.debug(f"{saved_token}")
        if saved_token and int(saved_token) == token:
            self.cache.delete(account)
            logger.debug(f"Email {account} has been verified")
            return True
        return False
