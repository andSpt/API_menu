from uuid import UUID

import sqlalchemy

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models import Dish, Submenu, Menu


from app.database import get_session
from app.repositories.messages import alredy_exist, not_found

class SubmenuRepository:

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
        self.name = 'submenu'
        self.model = Submenu


    async def get_all(self) -> list[Submenu]:
        stmt = select(Submenu).options(selectinload(Submenu.dishes))




