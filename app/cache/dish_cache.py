import json
from time import time
from uuid import UUID

from fastapi import Depends
from redis import asyncio as aioredis

from app.config import settings
from app.database import init_redis_pool
from app.schemas import DishResponse


class DishCache:
    def __init__(
        self,
        redis: aioredis.Redis = Depends(init_redis_pool),
    ) -> None:
        self.redis = redis
        self.all_dishes_key: str = "all_dishes"
        self.last_cache_update_key: str = "last_cache_update_dishes"

    async def set_dish_to_cache(self, dish_id: UUID, dish_data: DishResponse) -> None:
        await self.redis.hset(
            self.all_dishes_key, str(dish_id), dish_data.model_dump_json()
        )
        await self.redis.expire(name=self.all_dishes_key, time=settings.cache_ttl)

    async def get_cached_dish(self, dish_id: UUID) -> DishResponse | None:
        cached_dish: json = await self.redis.hget(self.all_dishes_key, str(dish_id))
        if cached_dish:
            return DishResponse.model_validate_json(cached_dish)

    async def get_all_dishes_from_cache(self) -> list[DishResponse] | None:
        last_update_time: str = await self.redis.get(self.last_cache_update_key)

        if last_update_time and time() - float(last_update_time) < settings.cache_ttl:
            all_dishes_in_cache: dict = await self.redis.hgetall(self.all_dishes_key)
            all_dishes: list[DishResponse] = [
                DishResponse.model_validate_json(value)
                for value in all_dishes_in_cache.values()
            ]
            return all_dishes

    async def set_all_dishes_to_cache(self, dishes: list[DishResponse]) -> None:
        for dish in dishes:
            await self.redis.hset(
                self.all_dishes_key, str(dish.id), dish.model_dump_json()
            )
        await self.redis.expire(self.all_dishes_key, time=settings.cache_ttl)
        await self.redis.set(self.last_cache_update_key, time())

    async def update_dish_in_cache(self, dish_id: UUID, dish_updated: DishResponse):
        await self.set_dish_to_cache(dish_id=dish_id, dish_data=dish_updated)
        await self.redis.expire(self.all_dishes_key, time=settings.cache_ttl)

    async def delete_dish_from_cache(self, dish_id: UUID):
        await self.redis.hdel(self.all_dishes_key, str(dish_id))
        await self.redis.expire(self.all_dishes_key, time=settings.cache_ttl)
