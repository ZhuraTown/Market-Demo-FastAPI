from http import HTTPStatus
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exception import ApplicationException
from src.db.models import User
from src.db.repositories.users import UserRepository
from src.dto.auth import CreateToken, ReadToken
from src.dto.user import CreateUser
from src.security.create_token import create_token
from src.security.password_hasher import hash_password, verify_password
from src.config import settings

class CreateUserUseCase:

    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session

    async def execute(self, data: CreateUser):
        # todo: add later push event to kafka
        found_email = await UserRepository.get_by_email(self.session, data.email)
        found_username = await UserRepository.get_by_username(self.session, data.username)
        if found_email or found_username:
            raise ApplicationException(status_code=HTTPStatus.BAD_REQUEST, detail="Email or username already exists")

        user = User(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password)
        )
        await UserRepository.create(self.session, user)
        await self.session.commit()
        return user

class AuthUserCase:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session


    async def execute(self, data: CreateToken) -> ReadToken:
        found_user = await UserRepository.get_by_username(self.session, data.username)
        if not found_user:
            raise ApplicationException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid login or password")

        if not verify_password(data.password, found_user.hashed_password):
            raise ApplicationException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid login or password")

        tokens: dict[str, Any] = {
            "access_token": (
                {"sub": str(found_user.id), "username": found_user.username, "type": "access"},
                settings.sec_ttl_access_token
            ),
            "refresh_token": (
                {"sub": str(found_user.id),"type": "refresh"},
                settings.sec_ttl_refresh_token,
            )
        }

        return ReadToken(
            access_token=create_token(*tokens["access_token"]),
            refresh_token=create_token(*tokens["refresh_token"])
        )