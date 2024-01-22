from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.database import get_session

from app.models import Submenu
from app.schemas import SubmenuResponse, SubmenuUpdate, SubmenuCreate
from app.repositories.submenu_repository import SubmenuRepository
class SubmenuService:

    def __init__(self, database_repository: SubmenuRepository = Depends()) -> None:
        self.database_repository = database_repository


    async def get_all(self, menu_id: UUID) -> list[SubmenuResponse]:
        return await self.database_repository.get_all(menu_id=menu_id)


    async def get_one(self, menu_id: UUID, submenu_id: UUID) -> SubmenuResponse:
        return await self.database_repository.get_submenu(menu_id=menu_id, submenu_id=submenu_id)

    async def create(self, menu_id: UUID, submenu_create: SubmenuCreate) -> SubmenuResponse:
        return await self.database_repository.create_submenu(menu_id=menu_id, submenu_create=submenu_create)

