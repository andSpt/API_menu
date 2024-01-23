from uuid import UUID

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from app.schemas import SubmenuResponse, SubmenuCreate, SubmenuUpdate
from app.services.submenu_service import SubmenuService

router = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus', tags=['Submenu'])


@router.get('/',
            response_model=list[SubmenuResponse],
            status_code=status.HTTP_200_OK,
            summary='Получить список подменю')
async def get_all(menu_id: UUID, submenu_service: SubmenuService = Depends()):
    """Получить список подменю с количеством блюд"""
    return await submenu_service.get_all(menu_id=menu_id)


@router.get('/{submenu_id}',
            response_model=SubmenuResponse,
            status_code=status.HTTP_200_OK,
            summary='Получить подменю')
async def get_menu(menu_id: UUID, submenu_id: UUID, submenu_service: SubmenuService = Depends()):
    """Получить подменю"""
    return await submenu_service.get_one(menu_id=menu_id, submenu_id=submenu_id)


@router.post('/',
             response_model=SubmenuResponse,
             status_code=status.HTTP_201_CREATED,
             summary='Создать подменю')
async def create_submenu(menu_id: UUID, submenu_create: SubmenuCreate, submenu_service: SubmenuService = Depends()):
    return await submenu_service.create(menu_id=menu_id, submenu_create=submenu_create)


@router.patch('/{submenu_id}',
              response_model=SubmenuResponse,
              status_code=status.HTTP_200_OK,
              summary='Обновить подменю')
async def update_submenu(menu_id: UUID,
                         submenu_id: UUID,
                         submenu_update: SubmenuUpdate,
                         submenu_service: SubmenuService = Depends()):
    return await submenu_service.update(menu_id=menu_id,
                                        submenu_id=submenu_id,
                                        submenu_update=submenu_update)


@router.delete('/{submenu_id}',
               status_code=status.HTTP_200_OK,
               summary='Удалить подменю')
async def delete_submenu(menu_id: UUID, submenu_id: UUID, submenu_service: SubmenuService = Depends()) -> JSONResponse:
    return await submenu_service.delete(menu_id=menu_id, submenu_id=submenu_id)