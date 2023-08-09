import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient

from app.main import app


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture
def prefix() -> str:
    return '/api/v1/menus'


@pytest.fixture
def menu_data() -> dict:
    return {'title': 'Menu title', 'description': 'Menu description'}


@pytest.fixture
def menu_update() -> dict:
    return {
        'title': 'Updated menu title',
        'description': 'Updated menu description'
    }


@pytest.fixture
def submenu_data() -> dict:
    return {'title': 'Submenu title', 'description': 'Submenu description'}


@pytest.fixture
def submenu_update() -> dict:
    return {
        'title': 'Updated submenu title',
        'description': 'Updated submenu description',
    }


@pytest.fixture
def dish_data() -> dict:
    return {
        'title': 'Dish title', 'description':
        'Dish description', 'price': '25.55'
    }


@pytest.fixture
def dish_data2() -> dict:
    return {
        'title': 'Dish title 2',
        'description': 'Dish description 2',
        'price': '13.50',
    }


@pytest.fixture
def dish_update() -> dict:
    return {
        'title': 'Updated dish title',
        'description': 'Updated dish description',
        'price': '15.10',
    }
