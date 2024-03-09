from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

import pytest
from app.repositories.menu_repository import Menu
from fastapi import Depends

from app.database import get_session
from app.repositories.menu_repository import MenuRepository

# menu_repository: MenuRepository = Depends()
import logging

# Конфигурация логирования
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
BASE_URL = "/api/v1/menus"

# menu_data: dict = {"title": "My menu 1", "description": "My menu description 1"}


async def test_get_all_menus(client):
    response = await client.get(f"{BASE_URL}")
    assert response.status_code == 200
    assert response.json() == []


async def test_create_menu(client, menu_data) -> None:
    response = await client.post(f"{BASE_URL}", json=menu_data)
    assert response.status_code == 201
    menu_id: UUID | str = response.json().get("id")
    assert menu_id is not None
    assert menu_data["title"] == response.json().get("title")
    assert menu_data["description"] == response.json().get("description")
    menu_data["id"] = menu_id

    # menu_in_db = get_menu_from_test_db
    # assert menu_data["title"] == menu_in_db.title
    # assert menu_data["description"] == menu_in_db.description


async def test_get_list_menus(client):
    response = await client.get(f"{BASE_URL}")
    assert response.status_code == 200
    assert len(response.json()) > 0


async def test_get_menu(client, menu_data):
    response = await client.get(f"{BASE_URL}/{menu_data.get('id')}")
    assert response.status_code == 200
    assert response.json().get("id") == menu_data.get("id")


async def test_update_menu(client, menu_data):
    update_data = {
        "title": "My updated menu 1",
        "description": "My updated menu description 1",
    }
    response = await client.patch(f"{BASE_URL}/{menu_data.get('id')}", json=update_data)
    assert response.status_code == 200

    menu_data["title"] = update_data["title"]
    menu_data["description"] = update_data["description"]

    update_response = await client.get(f"{BASE_URL}/{menu_data.get('id')}")
    assert update_response.status_code == 200
    assert update_response.json().get("id") == menu_data.get("id")
    assert update_response.json().get("title") == menu_data.get("title")
    assert update_response.json().get("description") == menu_data.get("description")


async def test_delete_menu(client, menu_data):
    response = await client.delete(f"{BASE_URL}/{menu_data.get('id')}")
    assert response.status_code == 200


async def test_get_empty_list_menus_after_delete(client):
    response = await client.get(BASE_URL)
    assert response.status_code == 200
    assert response.json() == []


async def test_get_menu_after_delete(client, menu_data):
    response = await client.get(f"{BASE_URL}/{menu_data.get('id')}")
    assert response.status_code == 404
    assert response.json().get("detail") == "menu not found"


async def test_get_empty_list_menu(client):
    response = await client.get(BASE_URL)
    assert response.status_code == 200
    assert response.json() == []
