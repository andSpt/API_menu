import json
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

    async def set_data_to_cache(
        self, menu_id: UUID, menu_data: MenuResponse, ttl: int = None
    ) -> None:
        await self.redis.set(
            name=str(menu_id),
            value=menu_data.model_dump_json(),
            ex=ttl or settings.cache_ttl,
        )

    async def get_cached_data(self, menu_id: UUID) -> MenuResponse | None:
        cached_data: json = await self.redis.get(name=str(menu_id))
        return (MenuResponse.model_validate_json(cached_data)) if cached_data else None

    async def clear_cache(self, menu_id: UUID) -> None:
        await self.redis.delete(str(menu_id))

    async def invalidate_cache_menu(
        self, menu_id: UUID, background_tasks: BackgroundTasks
    ) -> None:
        background_tasks.add_task(self.clear_cache, menu_id=menu_id)
