from fastapi import Depends

from src.api.deps.db import get_session
from src.domain.email_senders.fake_email_sender import FakeEmailSender
from src.domain.emails import EmailSenderService
from src.domain.users import UserEventProcessor




def get_email_notification_service(
    session=Depends(get_session),
) -> EmailSenderService:
    return EmailSenderService(
        session=session,
        sender=FakeEmailSender()
    )

def get_users_event_processor(
    session=Depends(get_session),
    email_service=Depends(get_email_notification_service),
) -> UserEventProcessor:
    return UserEventProcessor(session=session, email_service=email_service)