from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps.db import get_session
from src.domain.users import AuthUserCase
from src.dto.auth import ReadToken, CreateToken

router = APIRouter(
    prefix='/auth',
    tags=["auth"],
)

@router.post(
    "/login",
    status_code=HTTPStatus.OK,
    response_model=ReadToken
)
async def auth(
        data: CreateToken,
        session: Annotated[AsyncSession, Depends(get_session)]
) -> ReadToken:
    use_case = AuthUserCase(session=session)
    return await use_case.execute(data)

