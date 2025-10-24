
from src.api.deps.db import get_session
from src.config import settings
from fastapi import Depends

from src.consumers.deps import get_users_event_processor
from src.consumers.dto import UserEventV1
from faststream.kafka.fastapi import KafkaRouter, Logger

from src.domain.users import UserEventProcessor

router_v1 = KafkaRouter(
    settings.kafka_servers,
)



@router_v1.subscriber(
    settings.kafka_topic_users,

)
async def user_events_listen(
        msg: UserEventV1,
        logger: Logger,
        event_processor: UserEventProcessor = Depends(get_users_event_processor),
):
    logger.info(f"Event: {msg}")
    await event_processor.process_event(msg)
