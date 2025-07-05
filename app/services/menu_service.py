from uuid import UUID

from fastapi import BackgroundTasks, Depends
from fastapi.responses import JSONResponse

from app.cache.menu_cache import MenuCache
from app.models import Menu
from app.repositories.menu_repository import MenuRepository
from app.schemas import MenuCreate, MenuResponse, MenuUpdate


class MenuService:

    def __init__(
        self,
        background_tasks: BackgroundTasks,
        database_repository: MenuRepository = Depends(),
        menu_cache: MenuCache = Depends(),
    ) -> None:
        self.database_repository = database_repository
        self.menu_cache = menu_cache
        self.background_tasks = background_tasks

    async def get_all_menus(self) -> list[MenuResponse]:
        all_menus_in_cache: list[MenuResponse] = (
            await self.menu_cache.get_all_menus_from_cache()
        )
        if all_menus_in_cache:
            return all_menus_in_cache

        all_menus_in_db = await self.database_repository.get_all()
        self.background_tasks.add_task(
            self.menu_cache.set_all_menus_to_cache, all_menus_in_db
        )
        return all_menus_in_db

    async def get_menu(self, menu_id: UUID) -> MenuResponse:
        cached_menu: MenuResponse | None = await self.menu_cache.get_cached_menu(
            menu_id=menu_id
        )
        if cached_menu:
            return cached_menu
        menu_in_db: MenuResponse = await self.database_repository.get_menu(
            menu_id=menu_id
        )
        self.background_tasks.add_task(
            self.menu_cache.set_menu_to_cache, menu_id=menu_id, menu_data=menu_in_db
        )
        return menu_in_db

    async def create_menu(self, menu_create: MenuCreate) -> MenuResponse:
        menu: MenuResponse = await self.database_repository.create_menu(
            menu_create=menu_create
        )
        self.background_tasks.add_task(
            self.menu_cache.set_menu_to_cache, menu_id=menu.id, menu_data=menu
        )
        return menu

    async def update_menu(self, menu_update: MenuUpdate, menu_id: UUID) -> MenuResponse:
        menu_updated: MenuResponse = await self.database_repository.update_menu(
            menu_update=menu_update, menu_id=menu_id
        )
        self.background_tasks.add_task(
            self.menu_cache.update_menu_in_cache,
            menu_id=menu_id,
            menu_updated=menu_updated,
        )
        return menu_updated

    async def delete_menu(self, menu_id: UUID) -> JSONResponse:
        result = await self.database_repository.delete_menu(menu_id=menu_id)
        if result:
            self.background_tasks.add_task(
                self.menu_cache.delete_menu_from_cache, menu_id=menu_id
            )
        return result
