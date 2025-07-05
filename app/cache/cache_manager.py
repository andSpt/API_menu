# from aioredis import Redis
# from app.config import settings
# from fastapi import BackgroundTasks
#
# from app.schemas import MenuResponse
#
#
# class CacheManager:
#     def __init__(self, redis: Redis) -> None:
#         self.redis = redis
#
#     async def set_data_to_cache(self, key: UUID, data: Any, ttl: int = None) -> None:
#         await self.redis.set(str(key), str(data), ex=ttl or settings.cache_ttl)
#
#     async def get_cached_data(self, key_id: UUID) -> MenuResponse:
#         cached_data: json = await self.redis.get(str(key_id))
#         return MenuResponse.model_validate_json(cached_data) if cached_data else None
#
#     async def clear_cache(self, key: str) -> None:
#         await self.redis.delete(key)
#
#     async def invalidate_cache(self, key: str, background_tasks: BackgroundTasks) -> None:
#         # Добавляем задачу в фоновые задачи для инвалидации кэша
#         background_tasks.add_task(self.clear_cache, key)
