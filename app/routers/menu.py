from typing import List
from uuid import UUID

from app.models import Menu
from fastapi import APIRouter, Depends
from app.schemas import MenuSchema, MenuUpdateSchema, MenuCreateSchema
from app.services.menu_service import MenuService

    

router = APIRouter(prefix='/api/v1/menus', tags=['Menu'])


@router.get('/', response_model=list[MenuSchema], status_code=200)
async def get_list_menus(menu: MenuService = Depends()):
    '''Возвращает список меню с количеством всех подменю и блюд'''
    return await menu.get_all()


@router.get('/{menu_id}', response_model=MenuSchema)
async def get_menu(menu_id: UUID, menu: MenuService = Depends()):
    return await menu.get_menu(menu_id=menu_id)


@router.post('/', response_model=MenuSchema, status_code=201)
async def create_menu(menu_data: MenuCreateSchema, menu: MenuService = Depends()):
    '''Create menu'''
    return await menu.create_menu(menu_data)


    


@router.patch('/{menu_id}', response_model=MenuSchema)
async def update_patch(menu_id: UUID, menu_update: MenuUpdateSchema, menu: MenuService = Depends()):
    return await menu.update_menu(menu_update=menu_update, menu_id=menu_id)


# @router.delete('/{menu_id}')
# async def delete_menu():
#     pass
