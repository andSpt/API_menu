from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from app.database import get_session

from app.models import Submenu
from app.schemas import SubmenuResponse, SubmenuUpdate, SubmenuCreate
from app.repositories.submenu_repository import SubmenuRepository
from app.cache.submenu_cache import SubmenuCache


class SubmenuService:

    def __init__(
        self,
        background_tasks: BackgroundTasks,
        database_repository: SubmenuRepository = Depends(),
        submenu_cache: SubmenuCache = Depends(),
    ) -> None:
        self.database_repository = database_repository
        self.submenu_cache = submenu_cache
        self.background_tasks = background_tasks

    async def get_all_submenus(self, menu_id: UUID) -> list[SubmenuResponse]:
        all_submenus_in_cache: list[SubmenuResponse] = (
            await self.submenu_cache.get_all_submenus_from_cache()
        )
        if all_submenus_in_cache:
            return all_submenus_in_cache

        all_submenus_in_db: list[SubmenuResponse] = (
            await self.database_repository.get_all_submenus(menu_id=menu_id)
        )
        self.background_tasks.add_task(
            self.submenu_cache.set_all_submenus_to_cache, all_submenus_in_db
        )
        return all_submenus_in_db

    async def get_submenu(self, menu_id: UUID, submenu_id: UUID) -> SubmenuResponse:
        cached_submenu: SubmenuResponse = await self.submenu_cache.get_cached_submenu(
            submenu_id=submenu_id
        )
        if cached_submenu:
            return cached_submenu

        submenu_in_db: SubmenuResponse = await self.database_repository.get_submenu(
            menu_id=menu_id, submenu_id=submenu_id
        )
        self.background_tasks.add_task(
            self.submenu_cache.set_submenu_to_cache,
            submenu_id=submenu_id,
            submenu_data=submenu_in_db,
        )

        return submenu_in_db

    async def create_submenu(
        self, menu_id: UUID, submenu_create: SubmenuCreate
    ) -> SubmenuResponse:
        submenu: SubmenuResponse = await self.database_repository.create_submenu(
            menu_id=menu_id, submenu_create=submenu_create
        )
        self.background_tasks.add_task(
            self.submenu_cache.set_submenu_to_cache,
            submenu_id=submenu.id,
            submenu_data=submenu,
        )

        return submenu

    async def update_submenu(
        self, menu_id: UUID, submenu_id: UUID, submenu_update: SubmenuUpdate
    ) -> SubmenuResponse:
        submenu_updated: SubmenuResponse = (
            await self.database_repository.update_submenu(
                menu_id=menu_id, submenu_id=submenu_id, submenu_update=submenu_update
            )
        )
        self.background_tasks.add_task(
            self.submenu_cache.update_submenu_in_cache,
            submenu_id=submenu_id,
            submenu_updated=submenu_updated,
        )

        return submenu_updated

    async def delete_submenu(self, menu_id: UUID, submenu_id: UUID) -> JSONResponse:
        result = await self.database_repository.delete_submenu(
            menu_id=menu_id, submenu_id=submenu_id
        )
        if result:
            self.background_tasks.add_task(
                self.submenu_cache.delete_submenu_from_cache, submenu_id=submenu_id
            )
        return result
