from typing import List
from jwt.exceptions import InvalidTokenError
from uuid import UUID

from fastapi import Form
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)

from app.schemas import TokenInfo


from app.models import Menu
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from app.schemas import MenuCreate, MenuUpdate, MenuResponse
from app.services.menu_service import MenuService
from app.schemas import UserResponse, UserCreate
from app.services.user_service import UserService
from app.models import User
from app.database import get_session

from auth import utils as auth_utils

router = APIRouter(prefix="/api/v1/user", tags=["User"])
router_jwt = APIRouter(prefix="/api/v1/user/jwt", tags=["JWT"])

# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/jwt/login")


@router.post(
    "/", response_model=UserResponse, status_code=201, summary="Создать пользователя"
)
async def create_user(user_data: UserCreate, user_service: UserService = Depends()):
    return await user_service.create_user(user_data=user_data)


@router.get(
    "/", response_model=UserResponse, status_code=200, summary="Получить пользователя"
)
async def get_user(user_id: UUID, user_service: UserService = Depends()):
    return await user_service.get_user(user_id=user_id)


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(get_session),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
    )
    stmt = select(User).filter_by(username=username)
    user = await session.scalar(stmt)
    if not user:
        raise unauthed_exc

    if not auth_utils.validate_password(
        password=password, hashed_password=user.password.encode()
    ):
        raise unauthed_exc

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User inactive"
        )
    return user


@router_jwt.post("/login", response_model=TokenInfo)
async def auth_user_issue_jwt(user: UserResponse = Depends(validate_auth_user)):
    jwt_payload = {"sub": str(user.id), "username": user.username, "email": user.email}
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(access_token=token, token_type="Bearer")


async def get_current_token_payload(
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    token: str = Depends(oauth2_scheme),
) -> UserResponse:
    # token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error: {e}"
        )
    return payload


async def get_current_auth_user(
    user_service: UserService = Depends(),
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_session),
) -> UserResponse | None:
    id: str = payload.get("sub")
    user = await user_service.get_user(user_id=id)
    print(f"!!!{user.is_active}")
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid token (user not found)",
    )


async def get_current_active_auth_user(
    user: UserResponse = Depends(get_current_auth_user),
):
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )


@router_jwt.get("/user/")
async def auth_user_check_self_info(
    user: UserResponse = Depends(get_current_active_auth_user),
    payload: dict = Depends(get_current_token_payload),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "id": user.id,
        "logged_in_at": iat,
    }
