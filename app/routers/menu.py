from typing import List

from app.models import Menu
from fastapi import APIRouter, Depends
from app.schemas import MenuCreate, MenuOut
from app.services.menu_service import MenuService

    

router = APIRouter(prefix='/api/v1/menus', tags=['Menu'])


@router.get('/', response_model=list[MenuOut], status_code=200)
async def get_list_menus(menu: MenuService = Depends()):
    '''Возвращает список меню с количеством всех подменю и блюд'''
    return await menu.get_all()
               


@router.get('/{menu_id}')
async def get_menu():
    pass


@router.post('/', response_model=MenuOut, status_code=201)
async def create_menu(menu_data: MenuCreate, menu: MenuService = Depends()):
    '''Create menu'''
    return await menu.create_menu(menu_data)


    


@router.patch('/{menu_id}')
async def update_menu():
    pass


@router.delete('/{menu_id}')
async def delete_menu():
    pass
