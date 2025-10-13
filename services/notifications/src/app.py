from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from src.api.middlewares.x_request_id import RequestIDMiddleware
from src.utils.logger import setup_logging
from src.config import settings
from src.consumers.user_events import router_v1 as users_consumer_v1

MIDDLEWARES = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(RequestIDMiddleware),
]



ROUTES = [
    # notifications_v1,
    users_consumer_v1,
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

