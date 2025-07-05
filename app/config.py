import os
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 10


class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://postgres:postgres@db_app:6040/ylab"
    db_echo: bool = True
    redis_url: str = "redis://redis:6379"
    cache_ttl: int = 1
    rabbitmq_url: str = "pyamqp://guest@rabbitmq:5672//"
    test_db_url: str = (
        "postgresql+asyncpg://test_postgres:test_postgres@db_test:5432/test_ylab"
    )
    test_redis: str = "redis://test_redis:6379"
    test_rabbitmq: str = "pyamqp://guest@test_rabbitmq:5672//"
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
