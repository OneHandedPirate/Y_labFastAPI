import openpyxl
import requests

from app.core.settings import ADMIN_EXCEL_PATH, APP_HOST_PORT


def parse_excel(file_path: str) -> list:
    workbook = openpyxl.load_workbook(file_path, read_only=True)
    worksheet = workbook.active

    menus: list = []

    current_menu: dict = {}
    current_submenu: dict = {}

    for row in worksheet.iter_rows(min_row=1, values_only=True):
        if row[0]:
            if current_submenu:
                current_menu['submenus'].append(current_submenu)
            current_submenu = {}
            if current_menu:
                menus.append(current_menu)
            current_menu = {'title': row[1], 'description': row[2], 'submenus': []}
        elif type(row[1]) == int:
            if current_menu and current_submenu:
                current_menu['submenus'].append(current_submenu)
            current_submenu = {'title': row[2], 'description': row[3], 'dishes': []}
        elif type(row[2]) == int:
            current_dish = {'title': row[3], 'description': row[4], 'price': str(row[5])}
            current_submenu['dishes'].append(current_dish)

    if current_menu:
        if current_submenu:
            current_menu['submenus'].append(current_submenu)
        menus.append(current_menu)

    return menus


def fill_db_from_excel(json: list) -> dict:
    for menu in json:
        menu_obj = {'title': menu['title'], 'description': menu['description']}
        menu_resp = requests.post(f'http://{APP_HOST_PORT}/api/v1/menus', json=menu_obj).json()
        if menu['submenus']:
            for submenu in menu['submenus']:
                submenu_obj = {'title': submenu['title'], 'description': submenu['description']}
                submenu_resp = requests.post(
                    f'http://{APP_HOST_PORT}/api/v1/menus/{menu_resp["id"]}/submenus', json=submenu_obj).json()
                if submenu['dishes']:
                    for dish in submenu['dishes']:
                        dish_obj = {'title': dish['title'], 'description': dish['description'], 'price': dish['price']}
                        requests.post(
                            f'http://{APP_HOST_PORT}/api/v1/menus/{menu_resp["id"]}/submenus/{submenu_resp["id"]}/dishes', json=dish_obj).json()

    return {'detail': 'DB is synchronized'}


def sync_db():
    db_current_state = requests.get(f'http://{APP_HOST_PORT}/api/v1/menus/all_without_ids').json()
    excel_current_state = parse_excel(ADMIN_EXCEL_PATH)

    if db_current_state == excel_current_state:
        return {'detail': 'DB is synchronized'}

    elif not db_current_state:
        return fill_db_from_excel(excel_current_state)
