import logging

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from starlette.middleware.base import BaseHTTPMiddleware

from src.api.v1.services import UserService
from src.models import User
from src.utils.auth import TokenService
from src.utils.exceptions import UnauthorizedException

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/api/v1/sign-in/")


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exclude_paths: list[str] = None):
        super().__init__(app)
        self.exclude_paths = exclude_paths or []
        self.token_service: TokenService = TokenService()
        self.user_service: UserService = UserService()

    async def dispatch(self, request: Request, call_next):

        try:
            request_path = request.url.path
            logger.debug("In middlware")
            if any(request_path.startswith(exclude) for exclude in self.exclude_paths):
                return await call_next(request)

            token = await oauth2_scheme(request)
            try:
                decoded_token = self.token_service.decode_jwt(token)
            except JWTError:
                raise UnauthorizedException

            user_id = decoded_token.get("sub")
            company_id = decoded_token.get("company_id")

            if not user_id or not company_id:
                raise UnauthorizedException

            user: User = await self.user_service.get_by_id(user_id)
            logger.debug(f"{user=}")
            if not user and user.company_id != company_id:
                logger.debug("Not found or invalid token data")
                raise UnauthorizedException

            request.state.user = user

            logger.debug(f"user: {request.state.user=}")

            return await call_next(request)
        except (UnauthorizedException, HTTPException, JWTError) as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
            )
