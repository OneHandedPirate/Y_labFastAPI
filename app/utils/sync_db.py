from httpx import AsyncClient

from app.core.settings import ADMIN_EXCEL_PATH, APP_API_V1_URL
from app.utils.db_operations import db_to_tuple, sync_db_from_tuples
from app.utils.parse_excel import excel_to_list, excel_to_tuple


async def sync_db() -> str:
    async with AsyncClient() as ac:
        res = await ac.get(f'{APP_API_V1_URL}/menus/all')
        db_current_state = res.json()
        excel_current_state = excel_to_list(ADMIN_EXCEL_PATH)

        if db_current_state == excel_current_state:
            return 'DB is synchronized (equal)'

        return await sync_db_from_tuples(
            excel_to_tuple(ADMIN_EXCEL_PATH),
            db_to_tuple(db_current_state),
            ac=ac
        )
