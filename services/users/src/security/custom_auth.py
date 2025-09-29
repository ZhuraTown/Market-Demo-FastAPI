from typing import Annotated
from loguru import logger
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from starlette.authentication import AuthenticationBackend

from src.common.exception import BadTokenError
from src.security.http import HTTPBearer
from src.security.validate_token import verify_token


class CustomAuthentication(AuthenticationBackend):
    async def __call__(
        self,
        token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    ) -> dict:
        if not token.credentials:
            raise BadTokenError()

        return await self.auth(token.credentials)

    async def decode_jwt_token(self, token: str) -> dict:
        logger.debug("decode_jwt_token: Start decoding")
        res = verify_token(token)
        if not res:
            raise BadTokenError()
        return res

    async def validate_token(self, raw_token: str):
        parsed_token = await self.decode_jwt_token(raw_token)
        if parsed_token["type"] != "ACCESS_TOKEN":
            raise BadTokenError(detail="Некорректный тип токена")
        return parsed_token

    async def auth(self, token: str) -> dict:
        data = await self.validate_token(token)
        return data


custom_authentication = CustomAuthentication()
