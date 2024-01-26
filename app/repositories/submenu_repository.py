from uuid import UUID

import sqlalchemy

from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select, func, join, Select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models import Dish, Submenu, Menu
from sqlalchemy.engine import Result

from app.database import get_session
from app.schemas import SubmenuUpdate, SubmenuResponse, SubmenuCreate
from app.repositories.repository_utils import already_exist, not_found, successfully_deleted


class SubmenuRepository:

    @staticmethod
    def _get_basic_query_submenus() -> Select:
        stmt = (select(Submenu.id,
                       Submenu.title,
                       Submenu.description,
                       Submenu.menu_id,
                       func.count(Dish.id).label('dishes_count'))
                .join(Dish, Submenu.id == Dish.submenu_id, isouter=True)
                .group_by(Submenu.id)
                )
        return stmt

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.name = 'submenu'

    async def _check_exists_submenu_by_attr(self, submenu_create: SubmenuCreate, menu_id: UUID, attr: str) -> None:
        """Checking the menu object with the title attribute in the DB"""
        stmt = (
            select(Submenu)
            .filter(Submenu.menu_id == menu_id,
                    getattr(Submenu, attr) == getattr(submenu_create, attr)
                    )
        )
        submenu = await self.session.scalar(stmt)
        if submenu:
            already_exist(self.name)

    async def get_all(self, menu_id: UUID) -> list[SubmenuResponse]:
        stmt = (
            self._get_basic_query_submenus()
            .filter(Submenu.menu_id == menu_id)
        )
        result: Result = await self.session.execute(stmt)
        list_submenus = [SubmenuResponse.model_validate(row, from_attributes=True) for row in result]
        return list_submenus

    async def get_submenu(self, menu_id: UUID, submenu_id: UUID) -> SubmenuResponse:
        stmt = (
            self._get_basic_query_submenus()
            .filter(Menu.id == menu_id,
                    Submenu.id == submenu_id)
        )
        result: Result = await self.session.execute(stmt)
        submenu_row = result.first()
        if not submenu_row:
            not_found(self.name)
        submenu = SubmenuResponse.model_validate(submenu_row, from_attributes=True)
        return submenu

    async def create_submenu(self, menu_id: UUID, submenu_create: SubmenuCreate) -> SubmenuResponse:
        await self._check_exists_submenu_by_attr(menu_id=menu_id, submenu_create=submenu_create, attr='title')

        db_submenu = Submenu(menu_id=menu_id, **submenu_create.model_dump())
        self.session.add(db_submenu)
        await self.session.commit()
        await self.session.refresh(db_submenu)

        submenu = SubmenuResponse.model_validate(db_submenu, from_attributes=True)
        return submenu

    async def update_submenu(self, menu_id: UUID, submenu_id: UUID, submenu_update: SubmenuUpdate) -> SubmenuResponse:
        submenu: SubmenuResponse = await self.get_submenu(menu_id=menu_id, submenu_id=submenu_id)

        stmt = (
            update(Submenu)
            .filter(Submenu.id == submenu_id, Submenu.menu_id == menu_id)
            .values(**submenu_update.model_dump(exclude_unset=True))
        )
        await self.session.execute(stmt)
        await self.session.commit()

        for name, value in submenu_update.model_dump(exclude_unset=True).items():
            submenu.__setattr__(name, value)

        return submenu

    async def delete_submenu(self, menu_id: UUID, submenu_id: UUID) -> JSONResponse:
        await self.get_submenu(menu_id=menu_id, submenu_id=submenu_id)
        stmt = (
            delete(Submenu)
            .filter(Submenu.menu_id == menu_id, Submenu.id == submenu_id)
        )
        await self.session.execute(stmt)
        await self.session.commit()

        return successfully_deleted(self.name)
