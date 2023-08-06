from environ import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
    REDIS_HOST,
    REDIS_PORT,
)

DATABASE_URL = (
    f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
    f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
)

REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'

CACHE_EXPIRE_TIME = 3600

APP_DESC = """
At the moment the application provides the following functionality:

CRUD operations with **Menu**, **Submenu** and **Dish** entities.

CRUD operations are as follows:

* **Retrieve** entity;
* **Retrieve list** of entities;
* **Create** entity;
* **Update** entity;
* **Delete** entity;
"""

TAGS_META = [
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
