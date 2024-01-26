from uuid import UUID

from fastapi import Depends
import sqlalchemy
from sqlalchemy import select, Select, ScalarResult
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi.responses import JSONResponse
from app.models import Dish, Submenu, Menu
from app.database import get_session
from app.schemas import DishResponse, DishCreate, DishUpdate
from app.repositories.repository_utils import already_exist, not_found, successfully_deleted


class DishRepository:

    def __init__(self,
                 session: AsyncSession = Depends(get_session)
                 ) -> None:
        self.session = session
        self.name = 'dish'

    async def _check_exists_dish_by_attr(
            self,
            dish_create: DishCreate,
            submenu_id: UUID,
            attr: str
    ) -> None:
        """Checking the menu object with the title attribute in the DB"""
        stmt = select(Dish).filter(
            Dish.submenu_id == submenu_id,
            getattr(Dish, attr) == getattr(dish_create, attr)
        )
        submenu: ScalarResult | None = await self.session.scalar(stmt)
        if submenu:
            already_exist(self.name)

    async def get_all(
            self,
            submenu_id: UUID
    ) -> list[Dish]:
        stmt = select(Dish).filter(Dish.submenu_id == submenu_id)
        result: ScalarResult = await self.session.scalars(stmt)
        list_dishes = list(result.all())
        return list_dishes

    async def create_dish(
            self,
            submenu_id: UUID,
            dish_create: DishCreate
    ) -> Dish:
        await self._check_exists_dish_by_attr(
            submenu_id=submenu_id,
            dish_create=dish_create,
            attr='title'
        )
        dish = Dish(
            submenu_id=submenu_id,
            **dish_create.model_dump()
        )
        self.session.add(dish)
        await self.session.commit()
        await self.session.refresh(dish)
        return dish
    
    
    async def get_dish(
            self,
            submenu_id: UUID,
            dish_id: UUID
    ) -> Dish:
        stmt = select(Dish).filter(
            Dish.submenu_id == submenu_id,
            Dish.id == dish_id
        )
        dish = await self.session.scalar(stmt)

        if not dish:
            not_found(self.name)
        return dish


    async def update_dish(
            self,
            submenu_id: UUID,
            dish_id: UUID,
            dish_update: DishUpdate
    ) -> Dish:
        dish = await self.get_dish(
            submenu_id=submenu_id,
            dish_id=dish_id
        )

        for name, value in dish_update.model_dump(exclude_unset=True).items():
            setattr(dish, name, value)
        await self.session.commit()
        return dish


    async def delete_dish(self, submenu_id: UUID, dish_id: UUID) -> JSONResponse:
        dish = await self.get_dish(submenu_id=submenu_id, dish_id=dish_id)
        if not dish:
            not_found(self.name)

        await self.session.delete(dish)
        await self.session.commit()

        return successfully_deleted(self.name)

