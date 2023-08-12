import pytest
from httpx import AsyncClient


class TestCount:
    async def test_menu_create(self, ac: AsyncClient, prefix: str, menu_data: dict):
        resp = await ac.post(prefix, json=menu_data)
        data = resp.json()

        assert resp.status_code == 201
        assert data['title'] == menu_data['title']
        assert data['description'] == menu_data['description']
        assert data['id'] is not False
        pytest.count__menu_id = data['id']

    async def test_submenu_create(self, ac: AsyncClient, prefix: str, submenu_data: dict):
        resp = await ac.post(
            f'{prefix}/{pytest.count__menu_id}/submenus', json=submenu_data
        )
        data = resp.json()

        assert resp.status_code == 201
        assert data['title'] == submenu_data['title']
        assert data['description'] == submenu_data['description']
        assert data['id'] is not False
        pytest.count__submenu_id = data['id']

    async def test_dish1_create(self, ac: AsyncClient, prefix: str, dish_data: dict):
        resp = await ac.post(
            f'{prefix}/{pytest.count__menu_id}/submenus/'
            f'{pytest.count__submenu_id}/dishes',
            json=dish_data,
        )
        data = resp.json()

        assert resp.status_code == 201
        assert data['title'] == dish_data['title']
        assert data['description'] == dish_data['description']
        assert data['price'] == dish_data['price']
        assert data['id'] is not False
        pytest.count__dish1_id = data['id']

    async def test_dish2_create(self, ac: AsyncClient, prefix: str, dish_data2: dict):
        resp = await ac.post(
            f'{prefix}/{pytest.count__menu_id}/submenus/'
            f'{pytest.count__submenu_id}/dishes',
            json=dish_data2,
        )
        data = resp.json()

        assert resp.status_code == 201
        assert data['title'] == dish_data2['title']
        assert data['description'] == dish_data2['description']
        assert data['price'] == dish_data2['price']
        assert data['id'] is not False
        pytest.count__dish2_id = data['id']

    async def test_menu_details(self, ac: AsyncClient, prefix: str, menu_data: dict):
        resp = await ac.get(f'{prefix}/{pytest.count__menu_id}')
        data = resp.json()

        assert resp.status_code == 200
        assert data['title'] == menu_data['title']
        assert data['description'] == menu_data['description']
        assert data['id'] == pytest.count__menu_id
        assert data['submenus_count'] == 1
        assert data['dishes_count'] == 2

    async def test_submenu_details(self, ac: AsyncClient, prefix: str,
                                   submenu_data: dict):
        resp = await ac.get(
            f'{prefix}/{pytest.count__menu_id}/submenus/'
            f'{pytest.count__submenu_id}'
        )
        data = resp.json()

        assert resp.status_code == 200
        assert data['title'] == submenu_data['title']
        assert data['description'] == submenu_data['description']
        assert data['id'] == pytest.count__submenu_id
        assert data['dishes_count'] == 2

    async def test_all(self, ac: AsyncClient, prefix: str):
        resp = await ac.get(f'{prefix}/all')
        data = resp.json()

        assert resp.status_code == 200
        assert len(data) == 1
        assert len(data[0]['submenus']) == 1
        assert len(data[0]['submenus'][0]['dishes']) == 2

    async def test_submenu_delete(self, ac: AsyncClient, prefix: str):
        resp = await ac.delete(
            f'{prefix}/{pytest.count__menu_id}/submenus/'
            f'{pytest.count__submenu_id}'
        )

        assert resp.status_code == 200

    async def test_submenu_list(self, ac: AsyncClient, prefix: str):
        resp = await ac.get(f'{prefix}/{pytest.count__menu_id}/submenus')
        data = resp.json()

        assert resp.status_code == 200
        assert data == []

    async def test_all2(self, ac: AsyncClient, prefix: str):
        resp = await ac.get(f'{prefix}/all')
        data = resp.json()

        assert resp.status_code == 200
        assert len(data) == 1
        assert data[0]['submenus'] == []

    async def test_dish_list(self, ac: AsyncClient, prefix: str):
        resp = await ac.get(
            f'{prefix}/{pytest.count__menu_id}/submenus/'
            f'{pytest.count__submenu_id}/dishes'
        )
        data = resp.json()

        assert resp.status_code == 200
        assert data == []

    async def test_menu_details2(self, ac: AsyncClient, prefix: str, menu_data: dict):
        resp = await ac.get(f'{prefix}/{pytest.count__menu_id}')
        data = resp.json()

        assert resp.status_code == 200
        assert data['title'] == menu_data['title']
        assert data['description'] == menu_data['description']
        assert data['id'] == pytest.count__menu_id
        assert data['submenus_count'] == 0
        assert data['dishes_count'] == 0

    async def test_menu_delete(self, ac: AsyncClient, prefix: str):
        resp = await ac.delete(f'{prefix}/{pytest.count__menu_id}')

        assert resp.status_code == 200

    async def test_menu_list(self, ac: AsyncClient, prefix: str):
        resp = await ac.get(f'{prefix}')
        data = resp.json()

        assert resp.status_code == 200
        assert data == []

    async def test_all3(self, ac: AsyncClient, prefix: str):
        resp = await ac.get(f'{prefix}/all')
        data = resp.json()

        assert resp.status_code == 200
        assert data == []
