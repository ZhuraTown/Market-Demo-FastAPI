from loguru import logger


class FakeEmailSender:

    async def send_email(self, *args, **kwargs):
        logger.info(f"FAKE. Sending email...args: {args}, kwargs: {kwargs}")
