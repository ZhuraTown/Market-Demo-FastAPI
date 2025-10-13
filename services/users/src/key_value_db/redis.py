from redis.asyncio import Redis, ConnectionPool

from src.config import settings


class RedisClient:
    def __init__(self):
        self._client: Redis | None = None

    async def __call__(self):
        if not self._client:
            pool = ConnectionPool(
                max_connections=settings.redis_max_pool_connections,
                host=settings.redis_host,
                port=settings.redis_port,
                encoding="utf8",
                decode_responses=True,
            )
            self._client = Redis.from_pool(connection_pool=pool)
        return self._client


redis_client_singleton = RedisClient()
