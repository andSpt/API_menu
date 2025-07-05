from uuid import UUID

import sqlalchemy
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy import ScalarResult, Select, delete, select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_session
from app.models import Dish, Menu, Submenu
from app.repositories.repository_utils import (
    already_exist,
    not_found,
    successfully_deleted,
)
from app.schemas import DishCreate, DishResponse, DishUpdate


class DishRepository:

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session
        self.name = "dish"

    async def _check_exists_dish_by_attr(
        self, dish_create: DishCreate, submenu_id: UUID, attr: str
    ) -> None:
        """Checking the menu object with the title attribute in the DB"""
        stmt = select(Dish).filter(
            Dish.submenu_id == submenu_id,
            getattr(Dish, attr) == getattr(dish_create, attr),
        )
        submenu: ScalarResult | None = await self.session.scalar(stmt)
        if submenu:
            already_exist(self.name)

    async def get_all_dishes(self, submenu_id: UUID) -> list[DishResponse]:
        stmt = select(Dish).filter(Dish.submenu_id == submenu_id)
        result: ScalarResult = await self.session.scalars(stmt)
        list_dishes = [
            DishResponse.model_validate(row, from_attributes=True) for row in result
        ]
        return list_dishes

    async def create_dish(
        self, submenu_id: UUID, dish_create: DishCreate
    ) -> DishResponse:
        await self._check_exists_dish_by_attr(
            submenu_id=submenu_id, dish_create=dish_create, attr="title"
        )
        db_dish = Dish(submenu_id=submenu_id, **dish_create.model_dump())
        self.session.add(db_dish)
        await self.session.commit()
        await self.session.refresh(db_dish)

        dish = DishResponse.model_validate(db_dish, from_attributes=True)
        return dish

    async def get_dish(self, submenu_id: UUID, dish_id: UUID) -> DishResponse:
        stmt = select(Dish).filter(Dish.submenu_id == submenu_id, Dish.id == dish_id)
        db_dish = await self.session.scalar(stmt)
        if not db_dish:
            not_found(self.name)
        dish = DishResponse.model_validate(db_dish, from_attributes=True)
        return dish

    async def update_dish(
        self, submenu_id: UUID, dish_id: UUID, dish_update: DishUpdate
    ) -> DishResponse:
        dish = await self.get_dish(submenu_id=submenu_id, dish_id=dish_id)

        stmt = (
            update(Dish).filter(Dish.id == dish_id).values(**dish_update.model_dump())
        )
        await self.session.execute(stmt)
        await self.session.commit()

        for name, value in dish_update.model_dump().items():
            dish.__setattr__(name, value)

        return dish

    async def delete_dish(self, submenu_id: UUID, dish_id: UUID) -> JSONResponse:
        dish = await self.get_dish(submenu_id=submenu_id, dish_id=dish_id)
        if not dish:
            not_found(self.name)

        stmt = delete(Dish).filter(Dish.submenu_id == submenu_id, Dish.id == dish_id)
        await self.session.execute(stmt)
        await self.session.commit()

        return successfully_deleted(self.name)
