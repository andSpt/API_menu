from fastapi import Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.services.user_service import UserService
from auth import utils as auth_utils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/jwt/login")


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    user_service: UserService = Depends(),
):
    user = await user_service.get_user_by_username(username=username)
    if not user:
        auth_utils.error_unauthorized("Invalid username or password")

    if not auth_utils.validate_password(
        password=password, hashed_password=user.password
    ):
        auth_utils.error_unauthorized("Invalid username or password")

    if not user.is_active:
        auth_utils.error_forbidden("user inactive")
    return user


async def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> UserResponse:
    try:
        payload = auth_utils.decode_jwt(token=token)
    except InvalidTokenError:
        auth_utils.error_unauthorized("invalid token error")
    return payload


async def get_current_auth_user(
    user_service: UserService = Depends(),
    payload: dict = Depends(get_current_token_payload),
) -> UserResponse | None:
    user_id: str = payload.get("sub")
    user = await user_service.get_user(user_id=user_id)
    if user:
        return user
    auth_utils.error_unauthorized("invalid token")


async def get_current_active_auth_user(
    user: UserResponse = Depends(get_current_auth_user),
):
    if user.is_active:
        return user
    auth_utils.error_forbidden("user inactive")
