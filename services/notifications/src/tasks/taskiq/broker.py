from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend
from src.config import settings

redis_dsn = f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}"

redis_async_result = RedisAsyncResultBackend(
    redis_url=redis_dsn,
)

broker = ListQueueBroker(
    url=redis_dsn,
    result_backend=redis_async_result,
)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)
