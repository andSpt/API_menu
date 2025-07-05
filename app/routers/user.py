from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.schemas import TokenInfo, UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService
from auth import user_views
from auth import utils as auth_utils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/jwt/login")


router = APIRouter(prefix="/api/v1/user", tags=["User"])
router_jwt = APIRouter(prefix="/api/v1/user/jwt", tags=["JWT"])


@router.post(
    "", response_model=UserResponse, status_code=201, summary="Создать пользователя"
)
async def create_user(user_data: UserCreate, user_service: UserService = Depends()):
    return await user_service.create_user(user_data=user_data)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=200,
    summary="Получить пользователя",
)
async def get_user(user_id: UUID, user_service: UserService = Depends()):
    return await user_service.get_user(user_id=user_id)


@router.get(
    "",
    response_model=list[UserResponse],
    status_code=200,
    summary="Получить список пользователей",
)
async def get_all_users(user_service: UserService = Depends()):
    return await user_service.get_all_users()


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=200,
    summary="Обновить пользователя",
)
async def update_user(
    user_id: UUID, user_data: UserUpdate, user_service: UserService = Depends()
):
    return await user_service.update_user(user_id=user_id, user_update=user_data)


@router.delete(
    "/{user_id}",
    response_model=UserResponse,
    status_code=200,
    summary="Обновить пользователя",
)
async def delete_user(user_id: UUID, user_service: UserService = Depends()):
    return await user_service.delete_user(user_id=user_id)


@router_jwt.post("/login", response_model=TokenInfo)
async def auth_user_issue_jwt(
    user: UserResponse = Depends(user_views.validate_auth_user),
):
    jwt_payload = {"sub": str(user.id), "username": user.username, "email": user.email}
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(access_token=token, token_type="Bearer")


@router_jwt.get("/user")
async def auth_user_check_self_info(
    user: UserResponse = Depends(user_views.get_current_active_auth_user),
    payload: dict = Depends(user_views.get_current_token_payload),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "id": user.id,
        "logged_in_at": iat,
    }


@router.get("/confirm/{confirmation_token}")
async def request_confirmation(
    confirmation_token: str, user_service: UserService = Depends()
):
    await user_service.find_user_by_confirmation_token(
        confirmation_token=confirmation_token
    )
    return {"message": "Registration confirmed successfully"}
