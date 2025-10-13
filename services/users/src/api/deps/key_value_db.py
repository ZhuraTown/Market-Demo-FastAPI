from redis.asyncio import Redis

from src.key_value_db.redis import redis_client_singleton


async def get_redis() -> Redis:
    return await redis_client_singleton()