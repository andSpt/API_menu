from uuid import UUID

from fastapi import Depends
from app.schemas import UserCreate, UserResponse
from app.repositories.user_repository import UserRepository
from app.models import User


class UserService:
    def __init__(self, database_repository: UserRepository = Depends()):
        self.database_repository = database_repository

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        return await self.database_repository.create_user(user_data=user_data)

    async def get_user(self, user_id: UUID) -> UserResponse | None:
        return await self.database_repository.get_user(user_id=user_id)
