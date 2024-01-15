from uuid import UUID, uuid4

from typing import NoReturn
from fastapi import Depends, HTTPException, Query
from fastapi import status, HTTPException
from pydantic import UUID4

from sqlalchemy import Select, select, func, update, or_, distinct, outerjoin, join
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result, ScalarResult

from app.models import Menu, Submenu, Dish
from app.database import get_session
from app.schemas import MenuSchema, MenuCreateSchema, MenuUpdateSchema
from app.repositories.errors import alredy_exist, not_found


class MenuRepository:

    _BASIC_QUERY_MENUS = (select(Menu.id,
                   Menu.title,
                   Menu.description,
                   func.count(Submenu.id).label('submenus_count'),
                   func.count(Dish.id).label('dishes_count'))
            .join(Submenu, Menu.id == Submenu.menu_id, isouter=True)
            .join(Dish, Submenu.id == Dish.submenu_id, isouter=True)
            .group_by(Menu.id)
            )

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.model = Menu
        self.name = 'menu'


    async def check_exists_menu(self, menu_data: MenuCreateSchema) -> None:
        '''Checks there is an object with the same id and title parameters in the database'''
        stmt = select(Menu.id, Menu.title).filter(or_(Menu.id == menu_data.id, Menu.title == menu_data.title))
        object = await self.session.scalar(stmt)
        if object:
            alredy_exist(self.name)

    async def get_all(self) -> list[Menu]:
        result: Result = await self.session.execute(self._BASIC_QUERY_MENUS)
        menus = result.all()
        return menus

    async def get_menu(self, menu_id: UUID) -> Menu | None:
        result: Result = await self.session.execute(self._BASIC_QUERY_MENUS.filter(Menu.id == menu_id))
        menu = result.first()
        if not menu:
            alredy_exist(self.name)
        return menu


    async def create_menu(self, menu_data: MenuCreateSchema) -> Menu:
        await self.check_exists_menu(menu_data)

        db_menu = Menu(**menu_data.model_dump(exclude_unset=True))
        self.session.add(db_menu)
        await self.session.commit()
        await self.session.refresh(db_menu)

        db_menu.submenus_count = 0
        db_menu.dishes_count = 0
        return db_menu

    async def update_menu(self, menu_update: MenuUpdateSchema, menu: MenuSchema) -> Menu:
        menu_db = self.get_menu(menu=menu)
        for name, value in menu_update.model_dump(exclude_unset=True).items():
            setattr(menu, name, value)
        await self.session.commit()
        return menu






        # stmt = query(Menu).where(Menu.id == menu_id)
        #
        # stmt = select(Menu).where(Menu.id == menu_id)
        # result: Result = await self.session.execute(stmt)
        # db_menu = result.first()
        # if not db_menu:
        #     not_found(self.name)

# update_query = update(Menu).where(Menu.id == menu_id).values(menu_data.model_dump(exclude_unset=True))
# await self.session.execute(update_query)
# await self.session.commit()

# db_menu.title = menu_data.title
# db_menu.description = menu_data.description
# return db_menu
