from uuid import UUID, uuid4

from typing import Annotated, NoReturn
from fastapi import Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi import status, HTTPException
from pydantic import UUID4

from sqlalchemy import Select, select, func, update, or_, distinct, outerjoin, join, Row, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result, ScalarResult
from sqlalchemy.orm import selectinload, joinedload

from app.models import Menu, Submenu, Dish
from app.database import get_session
from app.schemas import MenuCreate, MenuUpdate, MenuResponse
from app.repositories.messages import already_exist, not_found, successfully_deleted


class MenuRepository:
    _BASIC_QUERY_MENUS = (
        select(Menu.id,
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

    async def check_exists_menu_by_title(self, menu_data: MenuCreate) -> None:
        """Checking the menu object with the title attribute in the DB"""
        stmt = select(Menu.title).filter(Menu.title == menu_data.title)
        menu: Menu = await self.session.scalar(stmt)
        if menu:
            already_exist(self.name)

    async def get_all(self) -> list[MenuResponse]:
        result: Result = await self.session.execute(self._BASIC_QUERY_MENUS)
        list_menu_response = [MenuResponse.model_validate(row, from_attributes=True) for row in result]
        return list_menu_response

    async def get_menu(self, menu_id: UUID) -> MenuResponse:
        stmt = self._BASIC_QUERY_MENUS.filter(Menu.id == menu_id)
        result: Result = await self.session.execute(stmt)
        menu_raw = result.first()
        if not menu_raw:
            not_found(self.name)
        menu_response = MenuResponse.model_validate(menu_raw, from_attributes=True)
        return menu_response

    async def create_menu(self, menu_data: MenuCreate) -> MenuResponse:
        await self.check_exists_menu_by_title(menu_data)
        db_menu = Menu(**menu_data.model_dump(exclude_unset=True))
        self.session.add(db_menu)
        await self.session.commit()
        await self.session.refresh(db_menu)
        menu_response = MenuResponse.model_validate(db_menu, from_attributes=True)
        return menu_response

    async def update_menu(self, menu_update: MenuUpdate, menu_id: UUID) -> MenuResponse:
        menu: MenuResponse = await self.get_menu(menu_id=menu_id)
        stmt = update(Menu).filter(Menu.id == menu_id).values(**menu_update.model_dump())
        await self.session.execute(stmt)
        await self.session.commit()
        for name, value in menu_update.model_dump().items():
            menu.__setattr__(name, value)

        return menu

    async def delete_menu(self, menu_id: UUID) -> JSONResponse:
        await self.get_menu(menu_id=menu_id)
        stmt = delete(Menu).filter(Menu.id == menu_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return successfully_deleted(self.name)
