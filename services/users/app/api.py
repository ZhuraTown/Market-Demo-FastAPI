from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from app.config import settings

MIDDLEWARES = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
]

from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


ROUTES = [
    router,
]

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.api.title,
        debug=True,
        middleware=MIDDLEWARES,
        root_path=settings.api.root_path,
    )

    for r in ROUTES:
        app.include_router(r)

    return app


app = create_app()




