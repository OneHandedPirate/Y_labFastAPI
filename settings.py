from environ import (POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD,
                     POSTGRES_PORT, POSTGRES_USER)

DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
