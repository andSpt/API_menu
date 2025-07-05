from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.schemas import SubmenuCreate, SubmenuResponse, SubmenuUpdate, UserResponse
from app.services.submenu_service import SubmenuService
from auth.user_views import get_current_active_auth_user

router = APIRouter(prefix="/api/v1/menus/{menu_id}/submenus", tags=["Submenu"])


@router.get(
    "",
    response_model=list[SubmenuResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить список подменю",
)
async def get_all_submenu(menu_id: UUID, submenu_service: SubmenuService = Depends()):
    """Получить список подменю с количеством блюд"""
    return await submenu_service.get_all_submenus(menu_id=menu_id)


@router.get(
    "/{submenu_id}",
    response_model=SubmenuResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить подменю",
)
async def get_submenu(
    menu_id: UUID, submenu_id: UUID, submenu_service: SubmenuService = Depends()
):
    """Получить подменю"""
    return await submenu_service.get_submenu(menu_id=menu_id, submenu_id=submenu_id)


@router.post(
    "",
    response_model=SubmenuResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать подменю",
)
async def create_submenu(
    menu_id: UUID,
    submenu_create: SubmenuCreate,
    submenu_service: SubmenuService = Depends(),
    current_user: UserResponse = Depends(get_current_active_auth_user),
):
    return await submenu_service.create_submenu(
        menu_id=menu_id, submenu_create=submenu_create
    )


@router.patch(
    "/{submenu_id}",
    response_model=SubmenuResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновить подменю",
)
async def update_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    submenu_update: SubmenuUpdate,
    submenu_service: SubmenuService = Depends(),
    current_user: UserResponse = Depends(get_current_active_auth_user),
):
    return await submenu_service.update_submenu(
        menu_id=menu_id, submenu_id=submenu_id, submenu_update=submenu_update
    )


@router.delete(
    "/{submenu_id}", status_code=status.HTTP_200_OK, summary="Удалить подменю"
)
async def delete_submenu(
    menu_id: UUID,
    submenu_id: UUID,
    submenu_service: SubmenuService = Depends(),
    current_user: UserResponse = Depends(get_current_active_auth_user),
) -> JSONResponse:
    return await submenu_service.delete_submenu(menu_id=menu_id, submenu_id=submenu_id)
