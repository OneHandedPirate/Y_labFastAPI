import requests

from app.core.settings import APP_HOST_PORT


def db_to_tuple(json: dict) -> tuple:
    menus: list = []
    submenus: list = []
    dishes: list = []

    for menu in json:
        menus.append({
            'id': menu['id'],
            'title': menu['title'],
            'description': menu['description']
        })
        for submenu in menu['submenus']:
            submenus.append({
                'menu_id': menu['id'],
                'id': submenu['id'],
                'title': submenu['title'],
                'description': submenu['description']
            })
            for dish in submenu['dishes']:
                dishes.append({
                    'menu_id': menu['id'],
                    'submenu_id': submenu['id'],
                    'id': dish['id'],
                    'title': dish['title'],
                    'description': dish['description'],
                    'price': dish['price']
                })

    return menus, submenus, dishes


def sync_db_from_tuples(excel: tuple, db: tuple) -> str:
    excel_menus, excel_submenus, excel_dishes = excel
    db_menus, db_submenus, db_dishes = db

    # Proccess menus
    if len(excel_menus) > len(db_menus):
        diff_menus = len(excel_menus) - len(db_menus)
        for menu in excel_menus[-diff_menus:]:
            requests.post(f'http://{APP_HOST_PORT}/api/v1/menus', json=menu)
        db_menus = db_to_tuple(requests.get(f'http://{APP_HOST_PORT}/api/v1/menus/all').json())[0]
    elif len(excel_menus) < len(db_menus):
        for menu in entities_to_delete(excel_menus, db_menus):
            requests.delete(f'http://{APP_HOST_PORT}/api/v1/menus/{menu["id"]}')
        db_menus, db_submenus, db_dishes = db_to_tuple(
            requests.get(f'http://{APP_HOST_PORT}/api/v1/menus/all').json()
        )
    for i in range(len(excel_menus)):
        if excel_menus[i] != db_menus[i]:
            requests.patch(
                f'http://{APP_HOST_PORT}/api/v1/menus/{excel_menus[i]["id"]}',
                json=excel_menus[i]
            )

    # Proccess submenus
    if len(excel_submenus) > len(db_submenus):
        diff_submenus = len(excel_submenus) - len(db_submenus)
        for submenu in excel_submenus[-diff_submenus:]:
            requests.post(
                f'http://{APP_HOST_PORT}/api/v1/menus/{submenu["menu_id"]}/submenus',
                json=submenu
            )
        db_submenus = db_to_tuple(
            requests.get(f'http://{APP_HOST_PORT}/api/v1/menus/all').json()
        )[1]
    elif len(excel_submenus) < len(db_submenus):
        for submenu in entities_to_delete(excel_submenus, db_submenus):
            requests.delete(
                f'http://{APP_HOST_PORT}/api/v1/menus/{submenu["menu_id"]}/submenus/{submenu["id"]}'
            )
        db_submenus, db_dishes = db_to_tuple(
            requests.get(f'http://{APP_HOST_PORT}/api/v1/menus/all').json()
        )[1:]
    for j in range(len(excel_submenus)):
        if excel_submenus[j] != db_submenus[j]:
            requests.patch(
                f'http://{APP_HOST_PORT}/api/v1/menus/{excel_submenus[j]["menu_id"]}'
                f'/submenus/{excel_submenus[j]["id"]}',
                json=excel_submenus[j]
            )

    # Proccess dishes
    if len(excel_dishes) > len(db_dishes):
        diff_dishes = len(excel_dishes) - len(db_dishes)
        for dish in excel_dishes[-diff_dishes:]:
            requests.post(f'http://{APP_HOST_PORT}/api/v1/menus/{dish["menu_id"]}'
                          f'/submenus/{dish["submenu_id"]}/dishes',
                          json=dish)
        db_dishes = db_to_tuple(
            requests.get(f'http://{APP_HOST_PORT}/api/v1/menus/all').json()
        )[2]
    elif len(excel_dishes) < len(db_dishes):
        for dish in entities_to_delete(excel_dishes, db_dishes):
            requests.delete(
                f'http://{APP_HOST_PORT}/api/v1/menus/{dish["menu_id"]}'
                f'/submenus/{dish["submenu_id"]}/dishes/{dish["id"]}'
            )
        db_dishes = db_to_tuple(
            requests.get(f'http://{APP_HOST_PORT}/api/v1/menus/all').json()
        )[-1]
    for k in range(len(excel_dishes)):
        if excel_dishes[k] != db_dishes[k]:
            requests.patch(
                f'http://{APP_HOST_PORT}/api/v1/menus/{excel_dishes[k]["menu_id"]}'
                f'/submenus/{excel_dishes[k]["submenu_id"]}/dishes/{excel_dishes[k]["id"]}',
                json=excel_dishes[k]
            )

    return 'DB synchronized (from tuples)'


def entities_to_delete(excel: dict, db: dict) -> list:
    to_del = []
    for entity in db:
        if entity['id'] not in [ent['id'] for ent in excel]:
            to_del.append(entity)
    return to_del
