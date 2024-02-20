from uuid import UUID
from fastapi import Depends
from fastapi.responses import JSONResponse


from app.repositories.menu_repository import MenuRepository
from app.models import Menu
from app.schemas import MenuCreate, MenuUpdate, MenuResponse
from app.cache.menu_cache import MenuCache


class MenuService:

    def __init__(
        self,
        database_repository: MenuRepository = Depends(),
        menu_cache: MenuCache = Depends(),
    ) -> None:
        self.database_repository = database_repository
        self.menu_cache = menu_cache

    async def get_all(self) -> list[MenuResponse]:
        return await self.database_repository.get_all()

    async def get_one(self, menu_id: UUID) -> MenuResponse:
        cached_menu = await self.menu_cache.get_cached_data(menu_id=menu_id)
        if cached_menu:
            print("get menu from cache")
            return cached_menu

        menu = await self.database_repository.get_menu(menu_id=menu_id)
        await self.menu_cache.set_data_to_cache(menu_id=menu_id, menu_data=menu)
        return menu

    async def create(self, menu_create: MenuCreate) -> MenuResponse:
        return await self.database_repository.create_menu(menu_create=menu_create)

    async def update(self, menu_update: MenuUpdate, menu_id: UUID) -> MenuResponse:
        return await self.database_repository.update_menu(
            menu_update=menu_update, menu_id=menu_id
        )

    async def delete(self, menu_id: UUID) -> JSONResponse:
        return await self.database_repository.delete_menu(menu_id=menu_id)
