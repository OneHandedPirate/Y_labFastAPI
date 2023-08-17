from environ import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
    RABBIT_HOST,
    RABBIT_PASSWORD,
    RABBIT_USER,
    RABBIT_VHOST,
    REDIS_HOST,
    REDIS_PORT,
)

DATABASE_URL: str = (
    f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
    f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
)

REDIS_URL: str = f'redis://{REDIS_HOST}:{REDIS_PORT}'

RABBITMQ_URL: str = f'amqp://{RABBIT_USER}:{RABBIT_PASSWORD}@{RABBIT_HOST}:5672/{RABBIT_VHOST}'

CACHE_EXPIRE_TIME: int = 3600

ADMIN_EXCEL_PATH: str = 'app/admin/Menu.xlsx'

APP_API_V1_URL: str = 'http://app:8000/api/v1'


APP_DESC: str = """
At the moment the application provides the following functionality:

CRUD operations with **Menu**, **Submenu** and **Dish** entities.

CRUD operations are as follows:

* **Retrieve** entity;
* **Retrieve list** of entities;
* **Create** entity;
* **Update** entity;
* **Delete** entity;
"""

TAGS_META: list = [
    {
        'name': 'Menu',
        'description': 'CRUD operations with **menu** entities.'
    },
    {
        'name': 'Submenu',
        'description': 'CRUD operations with **submenu** entities.'
    },
    {
        'name': 'Dish',
        'description': 'CRUD operations with **dish** entities.'
    }
]
