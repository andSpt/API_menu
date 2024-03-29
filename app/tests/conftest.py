import asyncio
from uuid import UUID

import pytest
import pytest_asyncio
from fastapi import Depends
from httpx import AsyncClient
from sqlalchemy import select, func, distinct
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine, async_session, get_session

from app.config import settings
from main import app
from app.models import Base, Menu, Submenu, Dish
from app.repositories.menu_repository import MenuRepository

# from sqlmodel import SQLModel

test_engine = create_async_engine(settings.test_db_url, echo=settings.db_echo)
#
# test_async_session = async_sessionmaker(
#     bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
# )


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def async_test_session() -> AsyncSession:
    session = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
        class_=AsyncSession,
        autoflush=False,
        autocommit=False,
    )

    async with session() as s:
        yield s


@pytest.fixture(scope="session", autouse=True)
async def prepare_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def menu_repository(async_test_session):
    """Фикстура для создания объекта репозитория меню"""
    return MenuRepository(session=async_test_session)


# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#
# async def drop_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


# @pytest.fixture(scope="session")
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture(scope="session")
def menu_data():
    """Фикстура данных для меню"""
    return {"title": "My menu 1", "description": "My menu description 1"}


@pytest.fixture(scope="session")
def submenu_data():
    """Фикстура данных для подменю"""
    return {"title": "My submenu 1", "description": "My submenu description 1"}


@pytest.fixture(scope="session")
def dish_data():
    """Фикстура данных для блюда"""
    return {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50",
    }


# @pytest.fixture(scope="function")
# async def get_menu_from_test_db(menu_data, async_test_session):
#     stmt = (
#         select(
#             Menu.id,
#             Menu.title,
#             Menu.description,
#             func.count(distinct(Submenu.id)).label("submenus_count"),
#             func.count(distinct(Dish.id)).label("dishes_count"),
#         )
#         .join(Submenu, Menu.id == Submenu.menu_id, isouter=True)
#         .join(Dish, Submenu.id == Dish.submenu_id, isouter=True)
#         .group_by(Menu.id)
#         .filter(Menu.id == menu_data["id"])
#     )
#     result = await async_test_session.execute(stmt)
#     print(f"+++++++++++{result.all()}+++++++++++++++++")
#     return result.all()


# @pytest.fixture(scope="function")
# async def get_menus_from_test_db(menu_repository: MenuRepository = Depends()):
#     await menu_repository.get_menu()


# async_session = async_sessionmaker(
#     bind=engine,
#     expire_on_commit=False,
#     class_=AsyncSession,
#     autoflush=False,
#     autocommit=False,
# )
# Base.metadata.bind = engine

#
# async_test_sessionmaker = async_sessionmaker(
#     bind=test_async_engine,
#     expire_on_commit=False,
#     class_=AsyncSession,
#     autoflush=False,
#     autocommit=False,
# )


# @pytest.fixture(scope="session", autouse=True)
# async def prepare_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


# @pytest.fixture(scope="session")
# def event_loop(request) -> AsyncGenerator:
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


# @pytest.fixture(scope="session")
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


# @pytest.fixture(autouse=True, scope="session")
# async def prepare_database():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
# @pytest.fixture(autouse=True, scope='module')
# @pytest.fixture(autouse=True, scope="module")
# async def prepare_database():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


#
# async def override_get_session() -> AsyncSession:
#     async with async_session() as session:
#         yield session
#
#
# app.dependency_overrides[get_session] = override_get_session


# @pytest.fixture(scope="function")
# async def session_override(app):
#     async_session = async_sessionmaker(
#         bind=engine,
#         expire_on_commit=False,
#         class_=AsyncSession,
#         autoflush=False,
#         autocommit=False,
#     )
#
#     async def get_session_override():
#         async with async_session() as session:
#             yield session
#
#     app.dependency_overrides[get_session] = get_session_override


#
#     # async with engine.begin() as conn:
#     #     await conn.run_sync(Base.metadata.drop_all)
#
#     # await engine.dispose()
#


# @pytest_asyncio.fixture(scope="function")
# async def client() -> AsyncGenerator:
#     async with AsyncClient(
#         app=app, base_url="http://127.0.0.1:8040/api/v1/menus"
#     ) as client:
#         yield client


# @pytest.fixture(scope="session")
# def engine():
#     return create_async_engine(settings.test_db_url, echo=True)


# @pytest.fixture(scope="session", autouse=True)
# async def test_async_engine():
#     test_engine = create_async_engine(settings.test_db_url, echo=True)
#     async with test_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield test_engine
#     async with test_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


# async_test_sessionmaker = async_sessionmaker(
#     bind=test_async_engine,
#     expire_on_commit=False,
#     class_=AsyncSession,
#     autoflush=False,
#     autocommit=False,
# )


# @pytest.fixture(scope="session")
# async def async_test_session(test_async_engine):
#


# @pytest.fixture(scope="function", autouse=True)
# async def session_override(app, connection_test):
#     async def get_db_override():
#         async with sessionmanager.session() as session:
#             yield session
#
#     app.dependency_overrides[get_db] = get_db_override
