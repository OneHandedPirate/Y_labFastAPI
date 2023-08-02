import pytest
from httpx import AsyncClient


class TestDish:
    async def test_menu_create(self, ac: AsyncClient, prefix, menu_data):
        resp = await ac.post(prefix, json=menu_data)
        data = resp.json()

        assert resp.status_code == 201
        assert data["title"] == menu_data["title"]
        assert data["description"] == menu_data["description"]
        assert data["id"] is not False
        pytest.dish__menu_id = data["id"]

    async def test_submenu_create(self, ac: AsyncClient, prefix, submenu_data):
        resp = await ac.post(
            f"{prefix}/{pytest.dish__menu_id}/submenus", json=submenu_data
        )
        data = resp.json()

        assert resp.status_code == 201
        assert data["title"] == submenu_data["title"]
        assert data["description"] == submenu_data["description"]
        assert data["id"] is not False
        pytest.dish__submenu_id = data["id"]

    async def test_dish_list(self, ac: AsyncClient, prefix):
        resp = await ac.get(
            f"{prefix}/{pytest.dish__menu_id}/submenus/"
            f"{pytest.dish__submenu_id}/dishes"
        )
        data = resp.json()

        assert resp.status_code == 200
        assert data == []

    async def test_dish_create(self, ac: AsyncClient, prefix, dish_data):
        resp = await ac.post(
            f"{prefix}/{pytest.dish__menu_id}/submenus/"
            f"{pytest.dish__submenu_id}/dishes",
            json=dish_data,
        )
        data = resp.json()

        assert resp.status_code == 201
        assert data["title"] == dish_data["title"]
        assert data["description"] == dish_data["description"]
        assert data["price"] == dish_data["price"]
        assert data["id"] is not False
        pytest.dish__dish_id = data["id"]

    async def test_dish_list2(self, ac: AsyncClient, prefix):
        resp = await ac.get(
            f"{prefix}/{pytest.dish__menu_id}/submenus/"
            f"{pytest.dish__submenu_id}/dishes"
        )
        data = resp.json()

        assert resp.status_code == 200
        assert data != []

    async def test_dish_details(self, ac: AsyncClient, prefix, dish_data):
        resp = await ac.get(
            f"{prefix}/{pytest.dish__menu_id}/submenus/"
            f"{pytest.dish__submenu_id}"
            f"/dishes/{pytest.dish__dish_id}"
        )
        data = resp.json()

        assert resp.status_code == 200
        assert data["title"] == dish_data["title"]
        assert data["description"] == dish_data["description"]
        assert data["price"] == dish_data["price"]
        assert data["id"] == pytest.dish__dish_id

    async def test_dish_update(self, ac: AsyncClient, prefix, dish_update):
        resp = await ac.patch(
            f"{prefix}/{pytest.dish__menu_id}/submenus/"
            f"{pytest.dish__submenu_id}"
            f"/dishes/{pytest.dish__dish_id}",
            json=dish_update,
        )
        data = resp.json()

        assert resp.status_code == 200
        assert data["title"] == dish_update["title"]
        assert data["description"] == dish_update["description"]
        assert data["price"] == dish_update["price"]
        assert data["id"] == pytest.dish__dish_id

    async def test_dish_details2(self, ac: AsyncClient, prefix, dish_update):
        resp = await ac.get(
            f"{prefix}/{pytest.dish__menu_id}/submenus/"
            f"{pytest.dish__submenu_id}"
            f"/dishes/{pytest.dish__dish_id}"
        )
        data = resp.json()

        assert resp.status_code == 200
        assert data["title"] == dish_update["title"]
        assert data["description"] == dish_update["description"]
        assert data["price"] == dish_update["price"]
        assert data["id"] == pytest.dish__dish_id

    async def test_dish_delete(self, ac: AsyncClient, prefix):
        resp = await ac.delete(
            f"{prefix}/{pytest.dish__menu_id}/submenus/"
            f"{pytest.dish__submenu_id}"
            f"/dishes/{pytest.dish__dish_id}"
        )

        assert resp.status_code == 200

    async def test_dish_list3(self, ac: AsyncClient, prefix):
        resp = await ac.get(
            f"{prefix}/{pytest.dish__menu_id}/submenus/"
            f"{pytest.dish__submenu_id}/dishes"
        )
        data = resp.json()

        assert resp.status_code == 200
        assert data == []

    async def test_dish_details3(self, ac: AsyncClient, prefix, dish_update):
        resp = await ac.get(
            f"{prefix}/{pytest.dish__menu_id}/submenus/"
            f"{pytest.dish__submenu_id}"
            f"/dishes/{pytest.dish__dish_id}"
        )
        data = resp.json()

        assert resp.status_code == 404
        assert data["detail"] == "dish not found"

    async def test_submenu_delete(self, ac: AsyncClient, prefix):
        resp = await ac.delete(
            f"{prefix}/{pytest.dish__menu_id}/submenus/"
            f"{pytest.dish__submenu_id}"
        )

        assert resp.status_code == 200

    async def test_submenu_list(self, ac: AsyncClient, prefix):
        resp = await ac.get(f"{prefix}/{pytest.dish__menu_id}/submenus")
        data = resp.json()

        assert resp.status_code == 200
        assert data == []

    async def test_menu_delete(self, ac: AsyncClient, prefix):
        resp = await ac.delete(f"{prefix}/{pytest.dish__menu_id}")

        assert resp.status_code == 200

    async def test_menu_list(self, ac: AsyncClient, prefix):
        resp = await ac.get(prefix)
        data = resp.json()

        assert resp.status_code == 200
        assert data == []
