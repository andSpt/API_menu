
from typing import AsyncIterator
from click import echo
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine



from app.config import settings



engine = create_async_engine(settings.db_url, echo=settings.db_echo)

async_session = async_sessionmaker(bind=engine,
                                   autoflush=False,
                                   autocommit=False,
                                   expire_on_commit=False)


async def get_session() -> AsyncIterator:
    async with async_session() as session:
        yield session




