from uuid import UUID

from fastapi import Depends, BackgroundTasks
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.repositories.user_repository import UserRepository
from app.models import User
from app.cache.user_cache import UserCache
from fastapi.responses import JSONResponse
from celery_app.tasks import send_confirmation_email


class UserService:
    def __init__(
        self,
        background_tasks: BackgroundTasks,
        database_repository: UserRepository = Depends(),
        user_cache: UserCache = Depends(),
    ):
        self.database_repository = database_repository
        self.user_cache = user_cache
        self.background_tasks = background_tasks

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        user: UserResponse = await self.database_repository.create_user(
            user_data=user_data
        )
        send_confirmation_email(
            username=user.username,
            confirmation_token=user.confirmation_token,
            user_email=user.email,
        )
        self.background_tasks.add_task(
            self.user_cache.set_user_to_cache, user_id=user.id, user_data=user
        )

        return user

    async def get_user(self, user_id: UUID) -> UserResponse | None:
        cached_user: UserResponse | None = await self.user_cache.get_cached_user(
            user_id=user_id
        )
        if cached_user:
            return cached_user
        user_in_db: UserResponse = await self.database_repository.get_user(
            user_id=user_id
        )
        self.background_tasks.add_task(
            self.user_cache.set_user_to_cache, user_id=user_id, user_data=user_in_db
        )
        return user_in_db

    async def update_user(self, user_id: UUID, user_update: UserUpdate):
        user_updated: UserResponse = await self.database_repository.update_user(
            user_id=user_id, user_update=user_update
        )
        self.background_tasks.add_task(
            self.user_cache.update_user_in_cache,
            user_id=user_id,
            user_updated=user_updated,
        )

        return user_updated

    async def delete_user(self, user_id: UUID) -> JSONResponse:
        result = await self.database_repository.delete_user(user_id=user_id)
        if result:
            self.background_tasks.add_task(
                self.user_cache.delete_user_from_cache, user_id=user_id
            )
        return result

    async def get_all_users(self) -> list[UserResponse]:
        all_users_cache: list[UserResponse] = (
            await self.user_cache.get_all_users_from_cache()
        )
        if all_users_cache:
            return all_users_cache

        all_users_in_db = await self.database_repository.get_all_users()
        self.background_tasks.add_task(
            self.user_cache.set_all_users_to_cache, all_users_in_db
        )
        return all_users_in_db

    async def get_user_by_username(self, username: str) -> UserResponse | None:
        cached_user: UserResponse = await self.user_cache.get_user_by_username(
            username=username
        )
        if cached_user:
            return cached_user
        user_in_db: UserResponse = await self.database_repository.get_user_by_username(
            username=username
        )
        self.background_tasks.add_task(
            self.user_cache.set_user_to_cache_by_username,
            username=username,
            user_data=user_in_db,
        )
        return user_in_db

    async def find_user_by_confirmation_token(self, confirmation_token: str) -> bool:
        return await self.database_repository.find_user_by_confirmation_token(
            confirmation_token=confirmation_token
        )
