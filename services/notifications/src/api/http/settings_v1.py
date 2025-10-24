from http import HTTPStatus

from fastapi import APIRouter, Depends
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps.auth_user import auth_user
from src.api.deps.db import get_session
from src.db.models import User

router_v1 = APIRouter(
    prefix='/v1/settings',
    tags=["settings"],
)


