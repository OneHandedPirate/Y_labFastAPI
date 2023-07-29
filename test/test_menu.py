import pytest
from httpx import AsyncClient


class TestMenu:
    async def test_menu_empty(self, ac: AsyncClient, prefix):
        resp = await ac.get(prefix)
        data = resp.json()

        assert resp.status_code == 200
        assert data == []

    async def test_menu_create(self, ac: AsyncClient, prefix, menu_data):
        resp = await ac.post(prefix, json=menu_data)
        data = resp.json()

        assert resp.status_code == 201
        assert data['title'] == menu_data['title']
        assert data['description'] == menu_data['description']
        assert data['id'] is not False
        pytest.menu__menu_id = data['id']

    async def test_menu_not_empty(self, ac: AsyncClient, prefix):
        resp = await ac.get(prefix)
        data = resp.json()

        assert resp.status_code == 200
        assert data != []

    async def test_menu_details(self, ac: AsyncClient, prefix, menu_data):
        resp = await ac.get(f'{prefix}/{pytest.menu__menu_id}')
        data = resp.json()

        assert resp.status_code == 200
        assert data['title'] == menu_data['title']
        assert data['description'] == menu_data['description']
        assert data['id'] == pytest.menu__menu_id

    async def test_menu_update(self, ac: AsyncClient, prefix, menu_update):

        resp = await ac.patch(f'{prefix}/{pytest.menu__menu_id}',
                              json=menu_update)

        data = resp.json()

        assert resp.status_code == 200
        assert data['title'] == menu_update['title']
        assert data['description'] == menu_update['description']
        assert data['id'] == pytest.menu__menu_id

    async def test_menu_details2(self, ac: AsyncClient, prefix, menu_update):
        resp = await ac.get(f'{prefix}/{pytest.menu__menu_id}')
        data = resp.json()

        assert resp.status_code == 200
        assert data['title'] == menu_update['title']
        assert data['description'] == menu_update['description']
        assert data['id'] == pytest.menu__menu_id

    async def test_menu_delete(self, ac: AsyncClient, prefix):
        resp = await ac.delete(f'{prefix}/{pytest.menu__menu_id}')

        assert resp.status_code == 200

    async def test_menu_empty2(self, ac: AsyncClient, prefix):
        resp = await ac.get(prefix)
        data = resp.json()

        assert resp.status_code == 200
        assert data == []

    async def test_menu_details_deleted(self, ac: AsyncClient, prefix):
        resp = await ac.get(f'{prefix}/{pytest.menu__menu_id}')
        data = resp.json()

        assert resp.status_code == 404
        assert data['detail'] == 'menu not found'

