# import pytest
# from fastapi.testclient import TestClient
# from main import app
#
#
# BASE_URL = "http://0.0.0.0:8000/api/v1/menus"
#
#
# @pytest.mark.run(order=9)
# def test_get_empty_list_dishes(client, menu_data, submenu_data):
#     response = client.get(
#         f"{BASE_URL}/{menu_data.get('id')}/submenus/{submenu_data.get('id')}/dishes"
#     )
#     assert response.status_code == 200
#     assert response.json() == []
#
#
# @pytest.mark.run(order=10)
# def test_create_dish(client, dish_data, menu_data, submenu_data):
#     response = client.post(
#         f"{BASE_URL}/{menu_data.get('id')}/submenus/{submenu_data.get('id')}/dishes",
#         json=dish_data,
#     )
#     assert response.status_code == 201
#     assert "id" in response.json()
#     assert dish_data["title"] == response.json().get("title")
#     assert dish_data["description"] == response.json().get("description")
#     assert dish_data["price"] == response.json().get("price")
#
#     dish_data["id"] = response.json().get("id")
#
#
# @pytest.mark.run(order=11)
# def test_get_list_dishes(client, menu_data, submenu_data):
#     response = client.get(
#         f"{BASE_URL}/{menu_data.get('id')}/submenus/{submenu_data.get('id')}/dishes"
#     )
#     assert response.status_code == 200
#     assert len(response.json()) > 0
#
#
# @pytest.mark.run(order=12)
# def test_get_dish(client, dish_data, menu_data, submenu_data):
#     response = client.get(
#         f"{BASE_URL}/{menu_data.get('id')}/submenus/{submenu_data.get('id')}/"
#         f"dishes/{dish_data.get('id')}"
#     )
#     assert response.status_code == 200
#     assert response.json().get("id") == dish_data.get("id")
#
#
# @pytest.mark.run(order=15)
# def test_update_dish(client, dish_data, menu_data, submenu_data):
#     update_data = {
#         "title": "My updated dish 1",
#         "description": "My updated dish description 1",
#         "price": "14.50",
#     }
#     response = client.patch(
#         f"{BASE_URL}/{menu_data.get('id')}/submenus/{submenu_data.get('id')}/"
#         f"dishes/{dish_data.get('id')}",
#         json=update_data,
#     )
#     assert response.status_code == 200
#
#     dish_data["title"] = update_data["title"]
#     dish_data["description"] = update_data["description"]
#     dish_data["price"] = update_data["price"]
#
#     update_response = client.get(
#         f"{BASE_URL}/{menu_data.get('id')}/submenus/{submenu_data.get('id')}/"
#         f"dishes/{dish_data.get('id')}"
#     )
#     assert update_response.status_code == 200
#     assert update_response.json().get("id") == dish_data.get("id")
#     assert update_response.json().get("title") == dish_data.get("title")
#     assert update_response.json().get("description") == dish_data.get("description")
#     assert update_response.json().get("price") == dish_data.get("price")
#
#
# @pytest.mark.run(order=16)
# def test_delete_dish(client, menu_data, submenu_data):
#     response = client.delete(
#         f"{BASE_URL}/{menu_data.get('id')}/submenus/{submenu_data.get('id')}/"
#         f"dishes/{dish_data.get('id')}"
#     )
#     assert response.status_code == 200
#
#
# @pytest.mark.run(order=17)
# def test_get_empty_list_dishes_after_delete(client, menu_data, submenu_data):
#     response = client.get(
#         f"{BASE_URL}/{menu_data.get('id')}/submenus/{submenu_data.get('id')}/dishes"
#     )
#     assert response.status_code == 200
#     assert response.json() == []
#
#
# @pytest.mark.run(order=18)
# def test_get_dish_after_delete(client, dish_data, menu_data, submenu_data):
#     response = client.get(
#         f"{BASE_URL}/{menu_data.get('id')}/submenus/{submenu_data.get('id')}/"
#         f"dishes/{dish_data.get('id')}"
#     )
#     assert response.status_code == 404
#     assert response.json().get("detail") == "dish not found"
