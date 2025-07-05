from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.models import Menu
from app.schemas import MenuCreate, MenuResponse, MenuUpdate, UserResponse
from app.services.menu_service import MenuService
from auth.user_views import get_current_active_auth_user

router = APIRouter(prefix="/api/v1/menus", tags=["Menu"])


@router.get(
    "",
    response_model=list[MenuResponse],
    status_code=200,
    summary="Получить список меню",
)
async def get_list_menus(menu_service: MenuService = Depends()):
    """Получить список меню с количеством всех подменю и блюд"""
    return await menu_service.get_all_menus()


@router.get("/{menu_id}", response_model=MenuResponse, summary="Получить меню")
async def get_menu(menu_id: UUID, menu_service: MenuService = Depends()):
    """Получить меню с количеством всех подменю и блюд"""
    return await menu_service.get_menu(menu_id=menu_id)


@router.post("", response_model=MenuResponse, status_code=201, summary="Создать меню")
async def create_menu(
    menu_data: MenuCreate,
    menu_service: MenuService = Depends(),
    current_user: UserResponse = Depends(get_current_active_auth_user),
):
    """Создать меню"""
    return await menu_service.create_menu(menu_data)


@router.patch(
    "/{menu_id}",
    response_model=MenuResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновить меню",
)
async def update_patch(
    menu_id: UUID,
    menu_update: MenuUpdate,
    menu_service: MenuService = Depends(),
    current_user: UserResponse = Depends(get_current_active_auth_user),
):
    """Обновить меню"""
    return await menu_service.update_menu(menu_update=menu_update, menu_id=menu_id)


@router.delete("/{menu_id}", status_code=status.HTTP_200_OK, summary="Удалить меню")
async def delete_menu(
    menu_id: UUID,
    menu_service: MenuService = Depends(),
    current_user: UserResponse = Depends(get_current_active_auth_user),
) -> JSONResponse:
    """Удалить меню"""
    return await menu_service.delete_menu(menu_id=menu_id)
