from httpx import AsyncClient

from app.core.settings import APP_API_V1_URL


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


async def sync_db_from_tuples(excel: tuple, db: tuple, ac: AsyncClient) -> str:
    excel_menus, excel_submenus, excel_dishes = excel
    db_menus, db_submenus, db_dishes = db

    # Proccess menus
    if menus_to_add := get_difference(db_menus, excel_menus):
        for menu in menus_to_add:
            await ac.post(f'{APP_API_V1_URL}/menus', json=menu)
        db_menus = db_to_tuple((await ac.get(f'{APP_API_V1_URL}/menus/all')).json())[0]
    if menus_to_del := get_difference(excel_menus, db_menus):
        for menu in menus_to_del:
            await ac.delete(f'{APP_API_V1_URL}/menus/{menu["id"]}')
        db_menus, db_submenus, db_dishes = db_to_tuple(
            (await ac.get(f'{APP_API_V1_URL}/menus/all')).json()
        )
    for i in range(len(excel_menus)):
        if excel_menus[i] != db_menus[i]:
            await ac.patch(
                f'{APP_API_V1_URL}/menus/{excel_menus[i]["id"]}',
                json=excel_menus[i]
            )

    # Proccess submenus
    if submenus_to_add := get_difference(db_submenus, excel_submenus):
        for submenu in submenus_to_add:
            await ac.post(
                f'{APP_API_V1_URL}/menus/{submenu["menu_id"]}/submenus',
                json=submenu
            )
        db_submenus = db_to_tuple(
            (await ac.get(
                f'{APP_API_V1_URL}/menus/all')).json()
        )[1]
    if subs_to_del := get_difference(excel_submenus, db_submenus):
        for submenu in subs_to_del:
            await ac.delete(
                f'{APP_API_V1_URL}/menus/{submenu["menu_id"]}/submenus/{submenu["id"]}'
            )
        db_submenus, db_dishes = db_to_tuple(
            (await ac.get(
                f'{APP_API_V1_URL}/menus/all')).json()
        )[1:]
    for j in range(len(excel_submenus)):
        if excel_submenus[j] != db_submenus[j]:
            await ac.patch(
                f'{APP_API_V1_URL}/menus/{excel_submenus[j]["menu_id"]}'
                f'/submenus/{excel_submenus[j]["id"]}',
                json=excel_submenus[j]
            )

    # Proccess dishes
    if dishes_to_add := get_difference(db_dishes, excel_dishes):
        for dish in dishes_to_add:
            await ac.post(
                f'{APP_API_V1_URL}/menus/{dish["menu_id"]}'
                f'/submenus/{dish["submenu_id"]}/dishes',
                json=dish)
        db_dishes = db_to_tuple(
            (await ac.get(f'{APP_API_V1_URL}/menus/all')).json())[2]
    if dishes_to_del := get_difference(excel_dishes, db_dishes):
        for dish in dishes_to_del:
            await ac.delete(
                f'{APP_API_V1_URL}/menus/{dish["menu_id"]}'
                f'/submenus/{dish["submenu_id"]}/dishes/{dish["id"]}'
            )
        db_dishes = db_to_tuple(
            (await ac.get(f'{APP_API_V1_URL}/menus/all')).json())[-1]
    for k in range(len(excel_dishes)):
        if excel_dishes[k] != db_dishes[k]:
            await ac.patch(
                f'{APP_API_V1_URL}/menus/{excel_dishes[k]["menu_id"]}'
                f'/submenus/{excel_dishes[k]["submenu_id"]}/dishes/{excel_dishes[k]["id"]}',
                json=excel_dishes[k]
            )

    return 'DB synchronized (from tuples)'


def get_difference(list1: list, list2: list) -> list:
    diff = []
    for entity in list2:
        if entity['id'] not in [ent['id'] for ent in list1]:
            diff.append(entity)
    return diff
