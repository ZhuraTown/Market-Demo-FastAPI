from typing import Annotated
from loguru import logger
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.authentication import AuthenticationBackend

from src.api.deps.db import get_session
from src.common.exception import BadTokenError
from src.db.models import User
from src.db.repositories.users import UserRepository
from src.security.http import HTTPBearer
from src.security.validate_token import verify_token


class CustomAuthentication(AuthenticationBackend):
    async def __call__(
        self,
        token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
        session: Annotated[AsyncSession, Depends(get_session)],
    ) -> User:
        if not token.credentials:
            raise BadTokenError()

        return await self.auth(token.credentials, session)

    async def decode_jwt_token(self, token: str) -> dict:
        logger.debug("decode_jwt_token: Start decoding")
        res = verify_token(token)
        if not res:
            raise BadTokenError()
        return res

    @staticmethod
    async def validate_token(raw_token: str) -> dict:
        decoded_token = verify_token(raw_token)
        if not decoded_token or decoded_token["type"] != "access":
            raise BadTokenError()
        return decoded_token

    async def auth(self, token: str, session) -> User:
        data = await self.validate_token(token)
        found_user = await UserRepository.get_by_id(session, int(data["sub"]))
        if not found_user or found_user.deleted_at is not None:
            logger.warning(f"User not found. {data["sub"]}")
            raise BadTokenError()
        return found_user


custom_authentication = CustomAuthentication()
