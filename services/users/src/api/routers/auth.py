from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.api.deps.db import get_session
from src.api.deps.key_value_db import get_redis
from src.domain.users import AuthUserCase, ResetPasswordUserCase, ConfirmResetPasswordCase
from src.dto.auth import ReadToken, CreateToken, ResetPassword, ConfirmResetPassword

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


@router.post("/reset-password", response_model=ReadToken)
async def reset_password(
        data: ResetPassword,
        redis: Annotated[Redis, Depends(get_redis)],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    use_case = ResetPasswordUserCase(session=session, redis=redis)
    await use_case.execute(data)

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={"message": "Email success send"},
    )

@router.put("/reset-password-confirm", status_code=HTTPStatus.OK)
async def reset_password_confirm(
        data: ConfirmResetPassword,
        redis: Annotated[Redis, Depends(get_redis)],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    use_case = ConfirmResetPasswordCase(session=session, redis=redis)
    await use_case.execute(data)
