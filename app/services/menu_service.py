from uuid import UUID
from fastapi import Depends
from fastapi.responses import JSONResponse



from app.repositories.menu_repository import MenuRepository
from app.models import Menu
from app.schemas import MenuCreate, MenuUpdate, MenuResponse


class MenuService:
    
    def __init__(self, database_repository: MenuRepository = Depends()) -> None:
        self.database_repository = database_repository


    async def get_all(self) -> list[MenuResponse]:
        return await self.database_repository.get_all()
    
    async def get_one(self, menu_id: UUID) -> MenuResponse:
        return await self.database_repository.get_menu(menu_id=menu_id)


    async def create(self, menu_create: MenuCreate) -> MenuResponse:
        return await self.database_repository.create_menu(menu_create=menu_create)
    

    async def update(self, menu_update: MenuUpdate, menu_id: UUID) -> MenuResponse:
        return await self.database_repository.update_menu(menu_update=menu_update, menu_id=menu_id)
    

    async def delete(self, menu_id: UUID) -> JSONResponse:
        return await self.database_repository.delete_menu(menu_id=menu_id)