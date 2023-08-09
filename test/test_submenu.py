import pytest
from httpx import AsyncClient


class TestSubmenu:
    async def test_menu_create(self, ac: AsyncClient, prefix: str, menu_data: dict):
        resp = await ac.post(prefix, json=menu_data)
        data = resp.json()

        assert resp.status_code == 201
        assert data['title'] == menu_data['title']
        assert data['description'] == menu_data['description']
        assert data['id'] is not False
        pytest.submenu__menu_id = data['id']

    async def test_submenu_list(self, ac: AsyncClient, prefix: str):
        resp = await ac.get(f'{prefix}/{pytest.submenu__menu_id}/submenus')
        data = resp.json()

        assert resp.status_code == 200
        assert data == []

    async def test_submenu_create(self, ac: AsyncClient, prefix: str, submenu_data: dict):
        resp = await ac.post(
            f'{prefix}/{pytest.submenu__menu_id}/submenus', json=submenu_data
        )
        data = resp.json()

        assert resp.status_code == 201
        assert data['title'] == submenu_data['title']
        assert data['description'] == submenu_data['description']
        assert data['id'] is not False
        pytest.submenu__submenu_id = data['id']

    async def test_submenu_list2(self, ac: AsyncClient, prefix: str):
        resp = await ac.get(f'{prefix}/{pytest.submenu__menu_id}/submenus')
        data = resp.json()

        assert resp.status_code == 200
        assert data != []

    async def test_submenu_details(self, ac: AsyncClient, prefix: str,
                                   submenu_data: dict):
        resp = await ac.get(
            f'{prefix}/{pytest.submenu__menu_id}/submenus/'
            f'{pytest.submenu__submenu_id}'
        )
        data = resp.json()

        assert resp.status_code == 200
        assert data['title'] == submenu_data['title']
        assert data['description'] == submenu_data['description']
        assert data['id'] == pytest.submenu__submenu_id

    async def test_submenu_update(self, ac: AsyncClient, prefix: str,
                                  submenu_update: dict):
        resp = await ac.patch(
            f'{prefix}/{pytest.submenu__menu_id}/submenus/'
            f'{pytest.submenu__submenu_id}',
            json=submenu_update,
        )
        data = resp.json()

        assert resp.status_code == 200
        assert data['title'] == submenu_update['title']
        assert data['description'] == submenu_update['description']
        assert data['id'] == pytest.submenu__submenu_id

    async def test_submenu_details2(self, ac: AsyncClient, prefix: str,
                                    submenu_update: dict):
        resp = await ac.get(
            f'{prefix}/{pytest.submenu__menu_id}/submenus/'
            f'{pytest.submenu__submenu_id}'
        )
        data = resp.json()

        assert resp.status_code == 200
        assert data['title'] == submenu_update['title']
        assert data['description'] == submenu_update['description']
        assert data['id'] == pytest.submenu__submenu_id

    async def test_submenu_delete(self, ac: AsyncClient, prefix: str):
        resp = await ac.delete(
            f'{prefix}/{pytest.submenu__menu_id}/submenus/'
            f'{pytest.submenu__submenu_id}'
        )

        assert resp.status_code == 200

    async def test_submenu_list3(self, ac: AsyncClient, prefix: str):
        resp = await ac.get(f'{prefix}/{pytest.submenu__menu_id}/submenus')
        data = resp.json()

        assert resp.status_code == 200
        assert data == []

    async def test_submenu_details3(self, ac: AsyncClient,
                                    prefix: str, submenu_update: dict):
        resp = await ac.get(
            f'{prefix}/{pytest.submenu__menu_id}/submenus/'
            f'{pytest.submenu__submenu_id}'
        )
        data = resp.json()

        assert resp.status_code == 404
        assert data['detail'] == 'submenu not found'

    async def test_menu_delete(self, ac: AsyncClient, prefix: str):
        resp = await ac.delete(f'{prefix}/{pytest.submenu__menu_id}')

        resp.status_code = 200

    async def test_menu_list(self, ac: AsyncClient, prefix: str):
        resp = await ac.get(f'{prefix}')
        data = resp.json()

        assert resp.status_code == 200
        assert data == []
