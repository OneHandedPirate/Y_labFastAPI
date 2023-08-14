import requests

from app.core.settings import ADMIN_EXCEL_PATH, APP_HOST_PORT
from app.utils.db_operations import db_to_tuple, sync_db_from_tuples
from app.utils.parse_excel import excel_to_list, excel_to_tuple


def sync_db() -> str:
    res = requests.get(f'http://{APP_HOST_PORT}/api/v1/menus/all')
    db_current_state = res.json()
    excel_current_state = excel_to_list(ADMIN_EXCEL_PATH)

    if db_current_state == excel_current_state:
        return 'DB is synchronized (equal)'

    return sync_db_from_tuples(
        excel_to_tuple(ADMIN_EXCEL_PATH),
        db_to_tuple(db_current_state)
    )
