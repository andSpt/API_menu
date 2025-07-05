from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.database import get_session
from app.models import Dish
from app.schemas import DishCreate, DishResponse, DishUpdate, UserResponse
from app.services.dish_service import DishService
from auth.user_views import get_current_active_auth_user

router = APIRouter(
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", tags=["Dish"]
)


@router.get(
    "",
    response_model=list[DishResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить список блюд",
)
async def get_all_dishes(submenu_id: UUID, dish_service: DishService = Depends()):
    return await dish_service.get_all_dishes(submenu_id=submenu_id)


@router.post(
    "",
    response_model=DishResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать блюдо",
)
async def create_dish(
    submenu_id: UUID,
    dish_create: DishCreate,
    dish_service: DishService = Depends(),
    current_user: UserResponse = Depends(get_current_active_auth_user),
):
    return await dish_service.create_dish(
        submenu_id=submenu_id, dish_create=dish_create
    )


@router.get(
    "/{dish_id}",
    response_model=DishResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить блюдо",
)
async def get_dish(
    submenu_id: UUID, dish_id: UUID, dish_service: DishService = Depends()
):
    return await dish_service.get_dish(submenu_id=submenu_id, dish_id=dish_id)


@router.patch(
    "/{dish_id}",
    response_model=DishResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновить блюдо",
)
async def update_dish(
    submenu_id: UUID,
    dish_id: UUID,
    dish_update: DishUpdate,
    dish_service: DishService = Depends(),
    current_user: UserResponse = Depends(get_current_active_auth_user),
):
    return await dish_service.update_dish(
        submenu_id=submenu_id, dish_id=dish_id, dish_update=dish_update
    )


@router.delete("/{dish_id}", status_code=status.HTTP_200_OK, summary="Удалить блюдо")
async def delete_dish(
    submenu_id: UUID,
    dish_id: UUID,
    dish_service: DishService = Depends(),
    current_user: UserResponse = Depends(get_current_active_auth_user),
) -> JSONResponse:
    return await dish_service.delete_dish(submenu_id=submenu_id, dish_id=dish_id)
