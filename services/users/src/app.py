import uvicorn
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from src.config import settings
from src.api.routers.users_v1 import router_v1 as users_v1

MIDDLEWARES = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
]



ROUTES = [
    users_v1,
]


def create_app() -> FastAPI:
    _app = FastAPI(
        title=settings.api_title,
        middleware=MIDDLEWARES,
        root_path=settings.api_root_path,
    )

    for r in ROUTES:
        _app.include_router(r)

    return _app


app = create_app()

