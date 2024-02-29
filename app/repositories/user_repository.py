from uuid import UUID

from fastapi import Depends

from app.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserCreate, UserResponse
from app.models import User
from auth import utils as auth_utils


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.name = "user"
        self.session = session

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        user = User(**user_data.model_dump())
        hashed_password: str = auth_utils.hash_password(user.password).decode("utf-8")
        setattr(user, "password", hashed_password)
        print(user.password)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        print(UserResponse.model_validate(user))
        return UserResponse.model_validate(user)

    async def get_user(self, user_id: UUID) -> UserResponse | None:
        user = await self.session.get(User, user_id)
        return UserResponse.model_validate(user)
