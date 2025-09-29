from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exception import ApplicationException
from src.db.models import User
from src.db.repositories.users import UserRepository
from src.dto.user import CreateUser
from src.security.password_hasher import hash_password


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
