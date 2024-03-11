from uuid import UUID
import pytest


BASE_URL = "/api/v1/menus"


@pytest.mark.order(1)
async def test_get_all_menus(client):
    response = await client.get(f"{BASE_URL}")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.order(2)
async def test_create_menu(client, menu_data) -> None:
    response = await client.post(f"{BASE_URL}", json=menu_data)
    assert response.status_code == 201
    menu_id: UUID | str = response.json().get("id")
    assert menu_id is not None
    assert menu_data["title"] == response.json().get("title")
    assert menu_data["description"] == response.json().get("description")
    menu_data["id"] = menu_id


@pytest.mark.order(3)
async def test_get_list_menus(client):
    response = await client.get(f"{BASE_URL}")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.order(4)
async def test_get_menu(client, menu_data):
    response = await client.get(f"{BASE_URL}/{menu_data.get('id')}")
    assert response.status_code == 200
    assert response.json().get("id") == menu_data.get("id")


@pytest.mark.order(21)
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


@pytest.mark.order(22)
async def test_delete_menu(client, menu_data):
    response = await client.delete(f"{BASE_URL}/{menu_data.get('id')}")
    assert response.status_code == 200


@pytest.mark.order(23)
async def test_get_empty_list_menus_after_delete(client):
    response = await client.get(BASE_URL)
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.order(24)
async def test_get_menu_after_delete(client, menu_data):
    response = await client.get(f"{BASE_URL}/{menu_data.get('id')}")
    assert response.status_code == 404
    assert response.json().get("detail") == "menu not found"


@pytest.mark.order(25)
async def test_get_empty_list_menu(client):
    response = await client.get(BASE_URL)
    assert response.status_code == 200
    assert response.json() == []
