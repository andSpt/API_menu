from uuid import UUID

from fastapi import Depends

from app.repositories.dish_repository import DishRepository
from app.models import Dish
from app.schemas import DishResponse, DishCreate, DishUpdate


class DishService:
    def __init__(self, database_repository: DishRepository = Depends()) -> None:
        self.database_repository = database_repository


    async def get_all(self, submenu_id: UUID) -> list[Dish]:
        return await self.database_repository.get_all(submenu_id=submenu_id)

    async def create(self, submenu_id: UUID, dish_create: DishCreate) -> Dish:
        return await self.database_repository.create_dish(submenu_id=submenu_id, dish_create=dish_create)


    async def get_dish(self, submenu_id: UUID, dish_id: UUID) -> Dish:
        return await self.database_repository.get_dish(submenu_id=submenu_id, dish_id=dish_id)
