from http import HTTPStatus
from typing import Any

from faststream.kafka.fastapi import KafkaBroker
from loguru import logger
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exception import ApplicationException
from src.db.models import User
from src.db.repositories.users import UserRepository
from src.dto.auth import CreateToken, ReadToken, ResetPassword, ConfirmResetPassword
from src.dto.user import CreateUser, UpdateUser
from src.events.dto import UserEventV1, EventType, UserData, MetaData, UserResetPasswordData
from src.security.create_token import create_token
from src.security.password_hasher import hash_password, verify_password
from src.config import settings
from src.security.validate_token import verify_token



class CreateUserUseCase:

    def __init__(
            self,
            session: AsyncSession,
            broker: KafkaBroker,
    ):
        self.broker = broker
        self.session = session

    async def execute(self, data: CreateUser):
        logger.info(f"Create new user {data}")
        found_user_with_email = await UserRepository.get_by_email(self.session, str(data.email))
        found_user_with_username = await UserRepository.get_by_username(self.session, data.username)
        if found_user_with_email or found_user_with_username:
            logger.warning(f"Error create new user{data}")
            raise ApplicationException(status_code=HTTPStatus.BAD_REQUEST, detail="Email or username already exists")

        user = User(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password)
        )
        await UserRepository.create(self.session, user)
        await self.session.commit()
        logger.info(f"Success created new user {data}")

        await self.broker.publish(
            UserEventV1(
                metadata=MetaData(event_id="event-id-1"),
                type=EventType.CREATED,
                data=UserData.model_validate(user, from_attributes=True),
            ), topic=settings.kafka_topic_users
        )

        return user

class AuthUserCase:

    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session

    async def execute(self, data: CreateToken) -> ReadToken:
        logger.info(f"auth user {data}")
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

class UpdateUserCase:

    def __init__(
            self,
            session: AsyncSession,
            broker: KafkaBroker,
    ):
        self.broker = broker
        self.session = session

    async def execute(self, pk: Any, data: UpdateUser):
        logger.info(f"Update user {pk}, data: {data}")
        found_user_with_email = await UserRepository.get_by_email(self.session, str(data.email))
        found_user_with_username = await UserRepository.get_by_username(self.session, data.username)
        if (
                (found_user_with_email  and found_user_with_email.id != pk)
                or (found_user_with_username and found_user_with_username.id != pk)
        ):
            logger.warning(f"Update user {pk}, data: {data}")
            raise ApplicationException(status_code=HTTPStatus.BAD_REQUEST, detail="Email or username already exists")

        await UserRepository.update(self.session, pk, data.model_dump(mode='json'))
        await self.session.commit()
        logger.info(f"Success updated user {pk}, data: {data}")
        return await UserRepository.get_by_id(self.session, pk)


class ResetPasswordUserCase:

    def __init__(
            self,
            session: AsyncSession,
            broker: KafkaBroker,
            redis: Redis,
    ):
        self.session = session
        self.redis = redis
        self.broker = broker

    async def execute(self, data: ResetPassword):
        logger.info(f"Reset password for email: {data.email}")
        found_user = await UserRepository.get_by_email(self.session, str(data.email))
        if not found_user:
            logger.warning(f"Email({data.email}) not found for reset-password")
            return

        reset_token = create_token(
            {"sub": str(found_user.id), "type": "reset_password"},
            60*15 # 15 minutes
        )
        if settings.debug:
            logger.info(f"Reset-password token: {reset_token}")

        await self.redis.setex(reset_token, settings.sec_ttl_reset_password_token, 1)
        await self.broker.publish(
            UserEventV1(
                metadata=MetaData(event_id="event-id-1"),
                type=EventType.RESET_PASSWORD,
                data=UserResetPasswordData(user_id=found_user.id, reset_url=f"/reset-password-confirm?token={reset_token}"),
            ), topic=settings.kafka_topic_users
        )
        return

class CheckConfirmResetPasswordTokenCase:

    def __init__(
            self,
            redis: Redis,
    ):
        self.redis = redis

    async def execute(self, reset_password_token: str):
        logger.info(f"Check reset_password_token: {reset_password_token}")

        found_token = await self.redis.get(reset_password_token)
        if not found_token:
            raise ApplicationException(status_code=HTTPStatus.BAD_REQUEST, detail="Token not found or not valid")

        token_data = verify_token(reset_password_token)
        if token_data.get("type") != "reset_password" or not token_data.get("sub"):
            raise ApplicationException(status_code=HTTPStatus.BAD_REQUEST, detail="Token not found or not valid")


class ConfirmResetPasswordCase:

    def __init__(
            self,
            session: AsyncSession,
            redis: Redis,
    ):
        self.redis = redis
        self.session = session

    async def execute(self, data: ConfirmResetPassword):
        logger.info(f"Reset password for token: {data.token}")

        found_token = await self.redis.getdel(data.token)
        if not found_token:
            raise ApplicationException(status_code=HTTPStatus.BAD_REQUEST, detail="Token not found or not valid")

        token_data = verify_token(data.token)
        if token_data.get("type") != "reset_password" or not token_data.get("sub"):
            raise ApplicationException(status_code=HTTPStatus.BAD_REQUEST, detail="Token not found or not valid")

        found_user = await UserRepository.get_by_id(self.session, int(token_data.get("sub")))
        if not found_user:
            raise ApplicationException(status_code=HTTPStatus.BAD_REQUEST, detail="Token not found or not valid")

        logger.info(f"User {found_user.id} change password")
        await UserRepository.update(
            self.session, found_user.id,
            {"hashed_password": hash_password(data.password)}
        )
        await self.session.commit()

