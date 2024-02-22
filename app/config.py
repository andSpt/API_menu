from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://postgres:postgres@127.0.0.1:6040/ylab"
    db_echo: bool = True
    redis_url: str = "redis://127.0.0.1:6379"
    cache_ttl: int = 500


settings = Settings()
