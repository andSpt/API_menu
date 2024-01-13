from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/ylab' 
    db_echo: bool = True


settings = Settings()






