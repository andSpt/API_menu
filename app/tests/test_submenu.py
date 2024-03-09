# import pytest
# from fastapi.testclient import TestClient
# from main import app
#
# BASE_URL = "/api/v1/menus"
#
#
# @pytest.mark.run(order=5)
# def test_get_empty_list_submenus(client, menu_data):
#     response = client.get(f"{BASE_URL}/{menu_data.get('id')}/submenus")
#     assert response.status_code == 200
#     assert response.json() == []
#
#
# @pytest.mark.run(order=6)
# def test_create_submenu(client, menu_data, submenu_data):
#     response = client.post(
#         f"{BASE_URL}/{menu_data.get('id')}/submenus", json=submenu_data
#     )
#     assert response.status_code == 201
#     assert "id" in response.json()
#     assert submenu_data["title"] == response.json().get("title")
#     assert submenu_data["description"] == response.json().get("description")
#
#     submenu_data["id"] = response.json().get("id")
#
#
# @pytest.mark.run(order=7)
# def test_get_list_submenus(client, menu_data):
#     response = client.get(f"{BASE_URL}/{menu_data.get('id')}/submenus")
#     assert response.status_code == 200
#     assert len(response.json()) > 0
#
#
# @pytest.mark.run(order=8)
# def test_get_submenu(client, menu_data, submenu_data):
#     response = client.get(
#         f"{BASE_URL}/{menu_data.get('id')}/submenus/{submenu_data.get('id')}"
#     )
#     assert response.status_code == 200
#     assert response.json().get("id") == submenu_data.get("id")
#
#
# @pytest.mark.run(order=14)
# def test_update_submenu(client, menu_data, submenu_data):
#     update_data = {
#         "title": "My updated submenu 1",
#         "description": "My updated submenu description 1",
#     }
#     response = client.patch(
#         f"{BASE_URL}/{menu_data.get('id')}/submenus/{submenu_data.get('id')}",
#         json=update_data,
#     )
#     assert response.status_code == 200
#
#     submenu_data["title"] = update_data["title"]
#     submenu_data["description"] = update_data["description"]
#
#     update_response = client.get(
#         f"{BASE_URL}/{menu_data.get('id')}/submenus/{submenu_data.get('id')}"
#     )
#     assert update_response.status_code == 200
#     assert update_response.json().get("id") == submenu_data.get("id")
#     assert update_response.json().get("title") == submenu_data.get("title")
#     assert update_response.json().get("description") == submenu_data.get("description")
#
#
# @pytest.mark.run(order=19)
# def test_delete_submenu(client, menu_data, submenu_data):
#     response = client.delete(
#         f"{BASE_URL}/{menu_data.get('id')}/submenus/{submenu_data.get('id')}"
#     )
#     assert response.status_code == 200
#
#
# @pytest.mark.run(order=20)
# def test_get_empty_list_submenus_after_delete(client, menu_data):
#     response = client.get(f"{BASE_URL}/{menu_data.get('id')}/submenus")
#     assert response.status_code == 200
#     assert response.json() == []
#
#
# @pytest.mark.run(order=21)
# def test_get_submenu_after_delete(client, submenu_data):
#     response = client.get(
#         f"{BASE_URL}/{menu_data.get('id')}/submenus/{submenu_data.get('id')}"
#     )
#     assert response.status_code == 404
#     assert response.json().get("detail") == "submenu not found"
