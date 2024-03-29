import json
from asyncio import sleep
from time import time
from uuid import UUID

from fastapi import BackgroundTasks, Depends
from redis import asyncio as aioredis

from app.config import settings
from app.database import init_redis_pool
from app.schemas import SubmenuResponse


class SubmenuCache:
    def __init__(
        self,
        redis: aioredis.Redis = Depends(init_redis_pool),
    ) -> None:
        self.redis = redis
        self.all_submenus_key: str = "all_submenus"
        self.last_cache_update_key: str = "last_cache_update_submenus"

    async def set_submenu_to_cache(
        self, submenu_id: UUID, submenu_data: SubmenuResponse
    ) -> None:
        await self.redis.hset(
            self.all_submenus_key, str(submenu_id), submenu_data.model_dump_json()
        )
        await self.redis.expire(name=self.all_submenus_key, time=settings.cache_ttl)

    async def get_cached_submenu(self, submenu_id: UUID) -> SubmenuResponse | None:
        cached_submenu: json = await self.redis.hget(
            self.all_submenus_key, str(submenu_id)
        )
        if cached_submenu:
            return SubmenuResponse.model_validate_json(cached_submenu)

    async def get_all_submenus_from_cache(self) -> list[SubmenuResponse] | None:
        last_update_time: str = await self.redis.get(self.last_cache_update_key)

        if last_update_time and time() - float(last_update_time) < settings.cache_ttl:
            all_submenus_in_cache: dict = await self.redis.hgetall(
                self.all_submenus_key
            )
            all_submenus: list[SubmenuResponse] = [
                SubmenuResponse.model_validate_json(value)
                for value in all_submenus_in_cache.values()
            ]
            return all_submenus

    async def set_all_submenus_to_cache(self, submenus: list[SubmenuResponse]) -> None:
        for submenu in submenus:
            await self.redis.hset(
                self.all_submenus_key, str(submenu.id), submenu.model_dump_json()
            )
        await self.redis.expire(self.all_submenus_key, time=settings.cache_ttl)
        await self.redis.set(self.last_cache_update_key, time())

    async def update_submenu_in_cache(
        self, submenu_id: UUID, submenu_updated: SubmenuResponse
    ):
        await self.set_submenu_to_cache(
            submenu_id=submenu_id, submenu_data=submenu_updated
        )
        await self.redis.expire(self.all_submenus_key, time=settings.cache_ttl)

    async def delete_submenu_from_cache(self, submenu_id: UUID):
        await self.redis.hdel(self.all_submenus_key, str(submenu_id))
        await self.redis.expire(self.all_submenus_key, time=settings.cache_ttl)
