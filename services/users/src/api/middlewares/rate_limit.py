from http import HTTPStatus

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.api.deps.key_value_db import get_redis

PER_SECONDS_LIMIT = 50

class RateLimitMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        redis = await get_redis()
        key = f"rate:{client_ip}:{request.url.path}"

        counter = await redis.incr(key)
        if counter == 1:
            await redis.expire(key, PER_SECONDS_LIMIT)
        elif counter > PER_SECONDS_LIMIT:
            return JSONResponse(status_code=HTTPStatus.TOO_MANY_REQUESTS, content="Too Many Requests")

        return await call_next(request)
