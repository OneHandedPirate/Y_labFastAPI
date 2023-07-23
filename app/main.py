from fastapi import FastAPI, Depends, status

from app.schemas import MenuCreate, MenuResponse, SubmenuResponse, DishCreate, DishResponse
from app.repositories.sqlalch import MenuRepository, SubmenuRepository, DishRepository


app = FastAPI(title='Cozy restaurant')


##################
# Menu Endpoints #
##################


@app.post('/api/v1/menus', description='Create menus',
          status_code=status.HTTP_201_CREATED,
          response_model=MenuResponse)
async def create_menu(menu: MenuCreate, menu_repo: MenuRepository = Depends()):
    return await menu_repo.create(menu.model_dump())


@app.get('/api/v1/menus/{menu_id}', response_model=MenuResponse)
async def get_menu(menu_id: int, menu_repo: MenuRepository = Depends()):
    return await menu_repo.get(menu_id)


@app.get('/api/v1/menus', response_model=list[MenuResponse])
async def get_menu_list(menu_repo: MenuRepository = Depends()):
    return await menu_repo.get_list()


@app.delete('/api/v1/menus/{menu_id}')
async def delete_menu(menu_id: int, menu_repo: MenuRepository = Depends()):
    return await menu_repo.delete(menu_id)


@app.patch('/api/v1/menus/{menu_id}', response_model=MenuResponse)
async def update_menu(menu_id: int, menu: MenuCreate,
                      menu_repo: MenuRepository = Depends()):
    return await menu_repo.update(menu_id, menu.model_dump())

#####################
# Submenu endpoints #
#####################


@app.post('/api/v1/menus/{menu_id}/submenus',
          status_code=status.HTTP_201_CREATED,
          response_model=SubmenuResponse)
async def create_submenu(menu_id: int, submenu: MenuCreate, submenu_repo: SubmenuRepository = Depends()):
    return await submenu_repo.create(submenu.model_dump(), menu_id)


@app.get('/api/v1/menus/{menu_id}/submenus',
         response_model=list[SubmenuResponse])
async def get_submenu_list(menu_id: int, submenu_repo: SubmenuRepository = Depends()):
    submenus = await submenu_repo.get_list(menu_id)
    return submenus


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}',
         response_model=SubmenuResponse)
async def get_submenu(menu_id: int, submenu_id: int,
                      submenu_repo: SubmenuRepository = Depends()):
    return await submenu_repo.get(submenu_id, menu_id)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}',
           response_model=SubmenuResponse)
async def update_submenu(menu_id: int, submenu_id: int, submenu: MenuCreate,
                         submenu_repo: SubmenuRepository = Depends()):
    return await submenu_repo.update(submenu_id, submenu.model_dump())


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
async def delete_menu(submenu_id: int,
                      submenu_repo: SubmenuRepository = Depends()):
    return await submenu_repo.delete(submenu_id)

####################
# Dishes endpoints #
####################


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
         response_model=DishResponse)
async def get_dish(submenu_id: int, dish_id: int,
                   dish_repo: DishRepository = Depends()):
    return await dish_repo.get(dish_id, submenu_id)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
         response_model=list[DishResponse])
async def get_dishes_list(menu_id: int, submenu_id: int, dish_repo: DishRepository = Depends()):
    return await dish_repo.get_list(submenu_id)


@app.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
          response_model=DishResponse, status_code=status.HTTP_201_CREATED)
async def create_dish(menu_id: int, submenu_id: int, dish: DishCreate,
                      dish_repo: DishRepository = Depends()):
    return await dish_repo.create(dish.model_dump(), submenu_id)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
           response_model=DishResponse)
async def update_dish(menu_id: int, submenu_id: int, dish_id: int,
                      dish: DishCreate, dish_repo: DishRepository = Depends()):
    return await dish_repo.update(dish_id, dish.model_dump())


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def delete_dish(menu_id: int, submenu_id, dish_id: int,
                      dish_repo: DishRepository = Depends()):
    return await dish_repo.delete(dish_id)




