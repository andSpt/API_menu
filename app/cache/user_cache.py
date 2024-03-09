import json
from asyncio import sleep
from time import time
from uuid import UUID

from fastapi import BackgroundTasks, Depends
from redis import asyncio as aioredis

from app.config import settings
from app.database import init_redis_pool
from app.schemas import UserResponse


class UserCache:
    def __init__(
        self,
        redis: aioredis.Redis = Depends(init_redis_pool),
    ) -> None:
        self.redis = redis
        self.all_users_key: str = "all_users"
        self.last_cache_update_key: str = "last_cache_update_users"

    async def set_user_to_cache(self, user_id: UUID, user_data: UserResponse) -> None:
        await sleep(4)
        await self.redis.hset(
            self.all_users_key, str(user_id), user_data.model_dump_json()
        )
        print(f"!!!!!! Add to cache user {user_id}!!!!!")
        await self.redis.expire(name=self.all_users_key, time=settings.cache_ttl)

    async def get_cached_user(self, user_id: UUID) -> UserResponse | None:
        cached_user: json = await self.redis.hget(self.all_users_key, str(user_id))
        if cached_user:
            print(f"!!!!user from cache {user_id}!!!")
            return UserResponse.model_validate_json(cached_user)

    async def get_all_users_from_cache(self) -> list[UserResponse] | None:
        last_update_time: str = await self.redis.get(self.last_cache_update_key)

        if last_update_time and time() - float(last_update_time) < settings.cache_ttl:
            all_users_in_cache: dict = await self.redis.hgetall(self.all_users_key)
            all_users: list[UserResponse] = [
                UserResponse.model_validate_json(value)
                for value in all_users_in_cache.values()
            ]
            print(f"!!!!user from cache {[user.id for user in all_users]}!!!")
            return all_users

    async def set_all_users_to_cache(self, users: list[UserResponse]) -> None:
        for user in users:
            await self.redis.hset(
                self.all_users_key, str(user.id), user.model_dump_json()
            )
        await self.redis.expire(self.all_users_key, time=settings.cache_ttl)
        await self.redis.set(self.last_cache_update_key, time())
        print(f"!!!!!! Add to cache all users !!!!!")

    async def update_user_in_cache(self, user_id: UUID, user_updated: UserResponse):
        await self.set_user_to_cache(user_id=user_id, user_data=user_updated)
        await self.redis.expire(self.all_users_key, time=settings.cache_ttl)

    async def delete_user_from_cache(self, user_id: UUID):
        await self.redis.hdel(self.all_users_key, str(user_id))
        await self.redis.expire(self.all_users_key, time=settings.cache_ttl)

    async def get_user_by_username(self, username: str) -> UserResponse | None:
        cached_user: json = await self.redis.hget(self.all_users_key, username)
        if cached_user:
            print(f"!!!!user from cache by username: {username}!!!")
            return UserResponse.model_validate_json(cached_user)

    async def set_user_to_cache_by_username(
        self, username: str, user_data: UserResponse
    ) -> None:
        await self.redis.hset(self.all_users_key, username, user_data.model_dump_json())
        print(f"!!!!!! Add to cache user by username: {username}!!!!!")
        await self.redis.expire(name=self.all_users_key, time=settings.cache_ttl)
