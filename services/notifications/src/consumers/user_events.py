
from src.api.deps.db import get_session
from src.config import settings
from fastapi import Depends
from src.consumers.dto import UserEventV1
from faststream.kafka.fastapi import KafkaRouter, Logger

from src.domain.users import UserService

router_v1 = KafkaRouter(
    settings.kafka_servers,
)



@router_v1.subscriber(
    settings.kafka_topic_users,

)
async def user_events_listen(
        msg: UserEventV1,
        logger: Logger,
        session=Depends(get_session),
):
    logger.info(f"Event: {msg}")
    await UserService.catch_event(session, msg)
