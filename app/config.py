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
    db_url: str = "postgresql+asyncpg://postgres:postgres@127.0.0.1:6040/ylab"
    db_echo: bool = True
    redis_url: str = "redis://127.0.0.1:6379"
    cache_ttl: int = 500
    test_db_url: str = (
        "postgresql+asyncpg://test_postgres:postgres@127.0.0.1:6050/test_ylab"
    )
    # test_redis: str = "redis://127.0.0.1:6479"
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
# print(type(settings.auth_jwt.private_key_path))
# print(settings.auth_jwt.private_key_path)
