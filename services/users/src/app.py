from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from src.api.middlewares.rate_limit import RateLimitMiddleware
from src.api.middlewares.x_request_id import RequestIDMiddleware
from src.config import settings
from src.api.routers.auth import router as auth_router
from src.api.routers.users_v1 import router_v1 as users_v1
from src.utils.logger import setup_logging

MIDDLEWARES = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(RequestIDMiddleware),
    Middleware(RateLimitMiddleware),
]



ROUTES = [
    users_v1,
    auth_router,
]


def create_app() -> FastAPI:
    setup_logging()
    _app = FastAPI(
        title=settings.api_title,
        middleware=MIDDLEWARES,
        root_path=settings.api_root_path,
    )

    for r in ROUTES:
        _app.include_router(r)

    return _app


app = create_app()

