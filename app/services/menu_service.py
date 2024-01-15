from uuid import UUID
from fastapi import Depends



from app.repositories.menu_repository import MenuRepository
from app.models import Menu
from app.schemas import MenuSchema, MenuUpdateSchema, MenuCreateSchema


class MenuService:
    
    def __init__(self, database_repository: MenuRepository = Depends()) -> None:
        self.database_repository = database_repository


    async def get_all(self) -> list[Menu]:
        return await self.database_repository.get_all()
    
    async def get_menu(self, menu_id: UUID):
        return await self.database_repository.get_menu(menu_id=menu_id)


    async def create_menu(self, menu_data: MenuCreateSchema) -> Menu:
        return await self.database_repository.create_menu(menu_data)
    

    async def update_menu(self, menu_update: MenuUpdateSchema, menu_id: UUID):
        return await self.database_repository.update_menu(menu_update=menu_update, menu_id=menu_id)
    

