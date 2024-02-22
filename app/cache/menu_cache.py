import json
from asyncio import sleep
from time import time
from uuid import UUID

from fastapi import BackgroundTasks, Depends
from redis import asyncio as aioredis

from app.config import settings
from app.database import init_redis_pool
from app.schemas import MenuResponse


class MenuCache:
    def __init__(
        self,
        redis: aioredis.Redis = Depends(init_redis_pool),
    ) -> None:
        self.redis = redis
        self.all_menus_key = "all_menus"
        self.last_cache_update_key = "last_cache_update_menus"

    async def set_menu_to_cache(self, menu_id: UUID, menu_data: MenuResponse):
        await sleep(4)
        await self.redis.hset(
            self.all_menus_key, str(menu_id), menu_data.model_dump_json()
        )
        print(f"!!!!!! Add to cache menu {menu_id}!!!!!")
        await self.redis.expire(name=self.all_menus_key, time=settings.cache_ttl)

    async def get_cached_menu(self, menu_id: UUID):
        cached_menu: json = await self.redis.hget(self.all_menus_key, str(menu_id))
        if cached_menu:
            print(f"!!!!Menu from cache {menu_id}!!!")
            return MenuResponse.model_validate_json(cached_menu)

    async def get_all_menus_from_cache(self) -> list[MenuResponse] | None:
        last_update_time: str = await self.redis.get(self.last_cache_update_key)

        if last_update_time and time() - float(last_update_time) < settings.cache_ttl:
            all_menus_in_cache: dict = await self.redis.hgetall(self.all_menus_key)
            all_menus: list[MenuResponse] = [
                MenuResponse.model_validate_json(value)
                for value in all_menus_in_cache.values()
            ]
            print(f"!!!!Menus from cache {[menu.id for menu in all_menus]}!!!")
            return all_menus

    async def set_all_menus_to_cache(self, menus: list[MenuResponse]) -> None:
        await sleep(4)
        for menu in menus:
            await self.redis.hset(
                self.all_menus_key, str(menu.id), menu.model_dump_json()
            )
        await self.redis.expire(self.all_menus_key, time=settings.cache_ttl)
        await self.redis.set(self.last_cache_update_key, time())
        print(f"!!!!!! Add to cache all menus !!!!!")

    async def update_menu_in_cache(self, menu_id: UUID, menu_updated: MenuResponse):
        await self.set_menu_to_cache(menu_id=menu_id, menu_data=menu_updated)
        await self.redis.expire(self.all_menus_key, time=settings.cache_ttl)

    async def delete_menu_from_cache(self, menu_id: UUID):
        await self.redis.hdel(self.all_menus_key, str(menu_id))
        await self.redis.expire(self.all_menus_key, time=settings.cache_ttl)
