
from fastapi import Depends



from app.repositories.menu_repository import MenuRepository
from app.models import Menu
from app.schemas import MenuCreate, MenuOut


class MenuService:
    
    def __init__(self, database_repository: MenuRepository = Depends()) -> None:
        self.database_repository = database_repository


    async def get_all(self) -> list[MenuOut]:
        return await self.database_repository.read_all()
    

    async def create_menu(self, menu_data: MenuCreate) -> Menu:
        return await self.database_repository.create_menu(menu_data)
    

    