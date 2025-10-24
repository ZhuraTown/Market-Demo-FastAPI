from typing import Protocol
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.users import UserRepository
from src.dto.email import EmailResetPasswordDTO, EmailWelcomeDTO
from src.db.models import EmailNotification
from src.db.repositories.notifications import NotificationsRepository

class EmailSenderInterface(Protocol):

    async def send_email(*args, **kwargs):
        pass



class EmailSenderService:

    def __init__(
            self,
            session: AsyncSession,
            sender: EmailSenderInterface):
        self.sender = sender
        self.session = session

    async def send_email_reset_password(
            self,
            data: EmailResetPasswordDTO
    ):
        logger.info(f"Send email reset password: {data.user_id} process starting")

        found_user = await UserRepository.get_by_id(self.session, data.user_id)
        if not found_user:
            logger.error(f"User not found: {data.user_id}")

        email = EmailNotification(
            recipient_email=found_user.email,
            user_id=found_user.id,
            header="Reset password!",
            subject=f"<div>Reset password bro!Go to link: {data.reset_password_url}</div>",
            source="users",
        )
        await NotificationsRepository[EmailNotification].create(self.session, email)
        await self.session.commit()

        await self.sender.send_email(email)

    async def send_email_welcome(
            self,
            data: EmailWelcomeDTO
    ):
        logger.info(f"Send email welcome: {data.email} process starting")

        email = EmailNotification(
            recipient_email=data.email,
            user_id=data.user_id,
            header="Welcome!",
            subject="<div>Welcome Bro!</div>",
            source="users",
        )
        await NotificationsRepository.create(self.session, email)
        await self.session.commit()

        await self.sender.send_email(email)

