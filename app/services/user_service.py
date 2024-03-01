from uuid import UUID

from fastapi import Depends
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.repositories.user_repository import UserRepository
from app.models import User


class UserService:
    def __init__(self, database_repository: UserRepository = Depends()):
        self.database_repository = database_repository

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        return await self.database_repository.create_user(user_data=user_data)

    async def get_user(self, user_id: UUID) -> UserResponse | None:
        return await self.database_repository.get_user(user_id=user_id)

    async def update_user(self, user_id: UUID, user_update: UserUpdate):
        return await self.database_repository.update_user(
            user_update=user_update, user_id=user_id
        )

    async def delete_user(self, user_id: UUID):
        return await self.database_repository.delete_user(user_id=user_id)

    async def get_all_users(self) -> list[UserResponse]:
        return await self.database_repository.get_all_users()

    async def get_user_by_username(self, username: str) -> UserResponse | None:
        return await self.database_repository.get_user_by_username(username=username)
