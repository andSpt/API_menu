from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from main import app

BASE_URL = "/api/v1/menus"


@pytest.mark.order(5)
async def test_get_empty_list_submenus(client, menu_data):
    response = await client.get(f"{BASE_URL}/{menu_data.get('id')}/submenus")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.order(6)
async def test_create_submenu(client, menu_data, submenu_data):
    response = await client.post(
        f"{BASE_URL}/{menu_data.get('id')}/submenus", json=submenu_data
    )
    assert response.status_code == 201

    submenu_id: UUID | str = response.json().get("id")
    assert submenu_id is not None

    assert submenu_data["title"] == response.json().get("title")
    assert submenu_data["description"] == response.json().get("description")

    submenu_data["id"] = submenu_id


@pytest.mark.order(7)
async def test_get_list_submenus(client, menu_data):
    response = await client.get(f"{BASE_URL}/{menu_data.get('id')}/submenus")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.order(8)
async def test_get_submenu(client, menu_data, submenu_data):
    response = await client.get(
        f"{BASE_URL}/{menu_data.get('id')}/submenus/{submenu_data.get('id')}"
    )
    assert response.status_code == 200
    assert response.json().get("id") == submenu_data.get("id")


@pytest.mark.order(17)
async def test_update_submenu(client, menu_data, submenu_data):
    update_data = {
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1",
    }
    response = await client.patch(
        f"{BASE_URL}/{menu_data.get('id')}/submenus/{submenu_data.get('id')}",
        json=update_data,
    )
    assert response.status_code == 200

    submenu_data["title"] = update_data["title"]
    submenu_data["description"] = update_data["description"]

    update_response = await client.get(
        f"{BASE_URL}/{menu_data.get('id')}/submenus/{submenu_data.get('id')}"
    )
    assert update_response.status_code == 200
    assert update_response.json().get("id") == submenu_data.get("id")
    assert update_response.json().get("title") == submenu_data.get("title")
    assert update_response.json().get("description") == submenu_data.get("description")


@pytest.mark.order(18)
async def test_delete_submenu(client, menu_data, submenu_data):
    response = await client.delete(
        f"{BASE_URL}/{menu_data.get('id')}/submenus/{submenu_data.get('id')}"
    )
    assert response.status_code == 200


@pytest.mark.order(19)
async def test_get_empty_list_submenus_after_delete(client, menu_data):
    response = await client.get(f"{BASE_URL}/{menu_data.get('id')}/submenus")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.order(20)
async def test_get_submenu_after_delete(client, menu_data, submenu_data):
    response = await client.get(
        f"{BASE_URL}/{menu_data.get('id')}/submenus/{submenu_data.get('id')}"
    )
    assert response.status_code == 404
    assert response.json().get("detail") == "submenu not found"
