from typing import Any
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import ScalarResult, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import User
from app.repositories.repository_utils import (
    already_exist,
    generate_confirmation_token,
    not_found,
    successfully_deleted,
)
from app.schemas import UserCreate, UserResponse, UserUpdate
from auth import utils as auth_utils


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.name = "user"
        self.session = session

    async def _check_exists_user_by_attr(
        self,
        attr_name: str,
        value: Any,
    ) -> None:
        """Checking the menu object with the title attribute in the DB"""
        if attr_name != "is_active":
            stmt = select(User).filter(getattr(User, attr_name) == value)
            user = await self.session.scalar(stmt)
            if user:
                already_exist(self.name)

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        user_data_to_dict: dict = user_data.model_dump()
        hashed_password: bytes = auth_utils.hash_password(user_data.password)
        user_data_to_dict["password"] = hashed_password
        for attr_name, value in user_data_to_dict.items():
            await self._check_exists_user_by_attr(attr_name, value)
        confirmation_token: str = generate_confirmation_token(
            email=user_data_to_dict.get("email")
        )
        user_data_to_dict["confirmation_token"] = confirmation_token
        user = User(**user_data_to_dict)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return UserResponse.model_validate(user)

    async def get_user(self, user_id: UUID) -> UserResponse | None:
        user = await self.session.get(User, user_id)
        if user:
            return UserResponse.model_validate(user)
        return not_found(self.name)

    async def update_user(self, user_update: UserUpdate, user_id: UUID) -> UserResponse:
        user: UserResponse = await self.get_user(user_id=user_id)
        user_update_to_dict: dict = user_update.model_dump(exclude_unset=True)
        if user_update_to_dict.get("password"):
            hashed_password: bytes = auth_utils.hash_password(
                user_update_to_dict.get("password")
            )
            user_update_to_dict["password"] = hashed_password

        for attr_name, value in user_update_to_dict.items():
            await self._check_exists_user_by_attr(attr_name, value)
            user.__setattr__(attr_name, value)
            print(f"!!!!!!!!!!{user}")
        stmt = update(User).filter(User.id == user_id).values(**user_update_to_dict)
        await self.session.execute(stmt)
        await self.session.commit()
        return user

    async def delete_user(self, user_id: UUID) -> JSONResponse:
        await self.get_user(user_id=user_id)
        stmt = delete(User).filter(User.id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return successfully_deleted(self.name)

    async def get_all_users(self) -> list[UserResponse]:
        stmt = select(User)
        result: ScalarResult = await self.session.scalars(stmt)
        list_users: list[UserResponse] = [
            UserResponse.model_validate(user) for user in result.all()
        ]
        return list_users

    async def get_user_by_username(self, username: str) -> UserResponse | None:
        stmt = select(User).filter_by(username=username)
        user = await self.session.scalar(stmt)
        if user:
            return UserResponse.model_validate(user)

    async def find_user_by_confirmation_token(self, confirmation_token: str) -> bool:
        stmt = select(User).filter_by(confirmation_token=confirmation_token)
        user: User = await self.session.scalar(stmt)
        if user:
            user.is_confirmed = True
            await self.session.commit()
            await self.session.refresh(user)
            return True
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ссылка для подтверждения регистрации не действительна. Возможно, вы уже подтвердили регистрацию.",
        )
