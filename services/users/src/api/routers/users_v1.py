from http import HTTPStatus

from fastapi import APIRouter, Depends
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps.auth_user import auth_user
from src.api.deps.db import get_session
from src.db.models import User
from src.domain.users import CreateUserUseCase
from src.dto.user import ReadUser, CreateUser

router_v1 = APIRouter(
    prefix='/v1/users',
    tags=["users"],
)



@router_v1.post(
    "/register",
    status_code=HTTPStatus.CREATED,
    response_model=ReadUser
)
async def create_user(
        data: CreateUser,
        session: Annotated[AsyncSession, Depends(get_session)]
) -> ReadUser:
    use_case = CreateUserUseCase(session=session)
    user = await use_case.execute(data)
    return ReadUser.model_validate(user, from_attributes=True)


@router_v1.get(
    "/me",
    response_model=ReadUser
)
async def get_me(
        user: Annotated[User, Depends(auth_user)],
):
    return ReadUser.model_validate(user, from_attributes=True)
