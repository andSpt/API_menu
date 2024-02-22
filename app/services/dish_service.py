from uuid import UUID

from fastapi import Depends, BackgroundTasks
from fastapi.responses import JSONResponse

from app.repositories.dish_repository import DishRepository
from app.models import Dish
from app.schemas import DishResponse, DishCreate, DishUpdate
from app.cache.dish_cache import DishCache


class DishService:
    def __init__(
        self,
        background_tasks: BackgroundTasks,
        database_repository: DishRepository = Depends(),
        dish_cache: DishCache = Depends(),
    ) -> None:
        self.database_repository = database_repository
        self.background_tasks = background_tasks
        self.dish_cache = dish_cache

    async def get_all_dishes(self, submenu_id: UUID) -> list[DishResponse]:
        all_dishes_in_cache: list[DishResponse] = (
            await self.dish_cache.get_all_dishes_from_cache()
        )
        if all_dishes_in_cache:
            return all_dishes_in_cache

        all_dishes_in_db: list[DishResponse] = (
            await self.database_repository.get_all_dishes(submenu_id=submenu_id)
        )
        self.background_tasks.add_task(
            self.dish_cache.set_all_dishes_to_cache, all_dishes_in_db
        )
        return all_dishes_in_db

    async def create_dish(
        self, submenu_id: UUID, dish_create: DishCreate
    ) -> DishResponse:
        dish: DishResponse = await self.database_repository.create_dish(
            submenu_id=submenu_id, dish_create=dish_create
        )
        self.background_tasks.add_task(
            self.dish_cache.set_dish_to_cache, dish_id=dish.id, dish_data=dish
        )
        return dish

    async def get_dish(self, submenu_id: UUID, dish_id: UUID) -> DishResponse:
        cached_dish: DishResponse = await self.dish_cache.get_cached_dish(
            dish_id=dish_id
        )
        if cached_dish:
            return cached_dish

        dish_in_db = await self.database_repository.get_dish(
            submenu_id=submenu_id, dish_id=dish_id
        )

        self.background_tasks.add_task(
            self.dish_cache.set_dish_to_cache, dish_id=dish_id, dish_data=dish_in_db
        )
        return dish_in_db

    async def update_dish(
        self, submenu_id: UUID, dish_id: UUID, dish_update: DishUpdate
    ) -> DishResponse:
        dish_updated: DishResponse = await self.database_repository.update_dish(
            submenu_id=submenu_id, dish_id=dish_id, dish_update=dish_update
        )
        self.background_tasks.add_task(
            self.dish_cache.update_dish_in_cache,
            dish_id=dish_id,
            dish_updated=dish_updated,
        )

        return dish_updated

    async def delete_dish(self, submenu_id: UUID, dish_id: UUID) -> JSONResponse:
        result = await self.database_repository.delete_dish(
            submenu_id=submenu_id, dish_id=dish_id
        )

        if result:
            self.background_tasks.add_task(
                self.dish_cache.delete_dish_from_cache, dish_id=dish_id
            )

        return result
