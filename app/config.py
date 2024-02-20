from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/ylab' 
    db_echo: bool = True
    redis_url: str = 'redis://127.0.0.1:6040'


settings = Settings()






