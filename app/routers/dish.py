from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi import status

from app.schemas import DishResponse, DishCreate, DishUpdate
from app.models import Dish
from app.database import get_session
from app.services.dish_service import DishService

router = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', tags=['Dish'])

@router.get('/',
            response_model=list[DishResponse],
            status_code=status.HTTP_200_OK,
            summary='Получить список блюд'
            )
async def get_all(submenu_id: UUID, dish_service: DishService = Depends()):
    return await dish_service.get_all(submenu_id=submenu_id)

@router.post('/',
             response_model=DishResponse,
             status_code=status.HTTP_201_CREATED,
             summary='Создать блюдо'
             )
async def create_dish(submenu_id: UUID, dish_create: DishCreate, dish_service: DishService = Depends()):
    return await dish_service.create(submenu_id=submenu_id, dish_create=dish_create)

@router.get('/{dish_id}',
            response_model=DishResponse,
            status_code=status.HTTP_200_OK,
            summary='Получить блюдо')
async def get_dish(submenu_id: UUID, dish_id: UUID, dish_service: DishService = Depends()):
    return await dish_service.get_dish(submenu_id=submenu_id, dish_id=dish_id)


