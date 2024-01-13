from uuid import UUID, uuid4


from typing import NoReturn
from fastapi import Depends, HTTPException
from fastapi import status, HTTPException
from pydantic import UUID4

from sqlalchemy import select, func, update, or_, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result, ScalarResult

from app.models import Menu, Submenu, Dish
from app.database import get_session
from app.schemas import MenuCreate, MenuOut
from app.repositories.errors import alredy_exist



class MenuRepository:
    
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.model = Menu
        self.name = 'menu'
    

    async def basic_menu_query(self, **kwargs) -> Result:
        '''Return join select all tables DB.
        Kwargs parametrs will add filtering to the query.
        Query containts count of submenus and dishes.'''

        stmt = select(
            Menu.id,
            Menu.title,
            Menu.description,
            func.count(Submenu.id).label('submenus_count'),
            func.count(Dish.id).label('dishes_count')
        ).filter_by(**kwargs).outerjoin(Submenu, Menu.id==Submenu.menu_id).outerjoin(Dish, Submenu.id==Dish.submenu_id).group_by(Menu.id)

        result = await self.session.execute(stmt)
        return result
    

    async def check_exists_menu(self, menu_data: MenuCreate) -> None:
        '''Checks there is an object with the same id and title parameters in the database'''
        
        stmt = select(Menu.id, Menu.title).filter(or_(Menu.id == menu_data.id, Menu.title == menu_data.title))
        object = await self.session.scalar(stmt)
        if object:
            alredy_exist(self.name)
    
    
    async def read_all(self) -> list[MenuOut]:
        '''Return list all menu into DB'''
        
        result: Result = await self.basic_menu_query()
        return result.all()
    

    async def create_menu(self, menu_data: MenuCreate) -> Menu:
        '''Create menu'''
        
        await self.check_exists_menu(menu_data)

        db_menu = Menu(id=menu_data.id if menu_data.id else uuid4(),
                       title=menu_data.title,
                       description=menu_data.description)
        self.session.add(db_menu)
        await self.session.commit()
        await self.session.refresh(db_menu)
        
        db_menu.submenus_count = 0
        db_menu.dishes_count = 0
        return db_menu
        

   




