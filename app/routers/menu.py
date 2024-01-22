from typing import List
from uuid import UUID

from app.models import Menu
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.schemas import MenuCreate, MenuUpdate, MenuResponse
from app.services.menu_service import MenuService

router = APIRouter(prefix='/api/v1/menus', tags=['Menu'])


@router.get('/',
            response_model=list[MenuResponse],
            status_code=200,
            summary='Получить список меню')
async def get_list_menus(menu: MenuService = Depends()):
    """Получить список меню с количеством всех подменю и блюд"""
    return await menu.get_all()


@router.get('/{menu_id}',
            response_model=MenuResponse,
            summary='Получить меню')
async def get_menu(menu_id: UUID,
                   menu: MenuService = Depends()):
    """Получить меню с количеством всех подменю и блюд"""
    return await menu.get_one(menu_id=menu_id)


@router.post('/',
             response_model=MenuResponse,
             status_code=201,
             summary='Создать меню')
async def create_menu(menu_data: MenuCreate,
                      menu: MenuService = Depends()):
    """Создать меню"""
    return await menu.create(menu_data)


@router.patch('/{menu_id}',
              response_model=MenuResponse,
              summary='Обновить меню')
async def update_patch(menu_id: UUID,
                       menu_update: MenuUpdate,
                       menu: MenuService = Depends()):
    """Обновить меню"""
    return await menu.update(menu_update=menu_update, menu_id=menu_id)


@router.delete('/{menu_id}',
               status_code=status.HTTP_200_OK,
               summary='Удалить меню')
async def delete_menu(menu_id: UUID,
                      menu: MenuService = Depends()) -> JSONResponse:
    """Удалить меню"""
    return await menu.delete(menu_id=menu_id)
