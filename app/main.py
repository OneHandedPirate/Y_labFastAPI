from uuid import UUID

from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Menu, Submenu, Dish
from app.schemas import MenuCreate, MenuResponse, SubmenuResponse, DishCreate, DishResponse
from app.db.session import get_async_session


app = FastAPI(title='Cozy restaurant')


####################
# Dishes endpoints #
####################

@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=DishResponse)
async def get_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, db: AsyncSession = Depends(get_async_session)):
    stmt = select(Dish).where(Dish.id == dish_id)
    res = await db.scalar(stmt)
    if res is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='dish not found')

    return res


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=list[DishResponse])
async def get_dishes_list(menu_id: UUID, submenu_id: UUID, db: AsyncSession = Depends(get_async_session)):
    stmt = select(Dish)
    res = (await db.execute(stmt)).scalars()
    return res


@app.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=DishResponse, status_code=status.HTTP_201_CREATED)
async def create_dish(menu_id: UUID, submenu_id: UUID, dish: DishCreate, db: AsyncSession = Depends(get_async_session)):
    stmt = select(Submenu).where(Submenu.menu_id == menu_id, Submenu.id == submenu_id)
    submenu_exists = (await db.scalar(stmt))
    if not submenu_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Submenu do not exist')
    new_dish = Dish(submenu_id=submenu_id, **dish.model_dump())
    db.add(new_dish)
    await db.commit()
    await db.refresh(new_dish)

    return new_dish


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=DishResponse)
async def update_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, dish: DishCreate, db: AsyncSession = Depends(get_async_session)):
    stmt = select(Submenu).where(Submenu.menu_id == menu_id, Submenu.id == submenu_id)
    submenu_exists = (await db.scalar(stmt))
    if not submenu_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Submenu do not exist')
    stmt2 = update(Dish).where(Dish.submenu_id == submenu_id, Dish.id == dish_id).values(title=dish.title,
                                                                                         description=dish.description,
                                                                                         price=dish.price)
    await db.execute(stmt2)
    await db.commit()

    after_update = await db.scalar(select(Dish).where(Dish.id == dish_id))
    return after_update


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
async def delete_dish(menu_id: UUID, submenu_id, dish_id: UUID, db: AsyncSession = Depends(get_async_session)):
    stmt = delete(Dish).where(Dish.id == dish_id)
    await db.execute(stmt)
    await db.commit()

    return {'detail': 'successfully deleted'}

#####################
# Submenu endpoints #
#####################


@app.post('/api/v1/menus/{menu_id}/submenus', status_code=status.HTTP_201_CREATED,
          response_model=SubmenuResponse)
async def create_submenu(menu_id: UUID, submenu: MenuCreate, db: AsyncSession = Depends(get_async_session)):
    stmt = select(Submenu).filter(Submenu.title == submenu.title)
    submenu_from_db = (await db.execute(stmt)).scalar()
    if submenu_from_db is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Submenu with the title {submenu.title} already exists in database')
    new_submenu = Submenu(menu_id=menu_id, **submenu.model_dump())
    db.add(new_submenu)
    await db.commit()
    await db.refresh(new_submenu)
    return new_submenu


@app.get('/api/v1/menus/{menu_id}/submenus', response_model=list[SubmenuResponse])
async def get_submenu_list(menu_id: UUID, db: AsyncSession = Depends(get_async_session)):
    stmt = select(Submenu).filter(Submenu.menu_id == menu_id)
    submenu_list = (await db.execute(stmt)).scalars()
    return submenu_list


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=SubmenuResponse)
async def get_submenu(menu_id: UUID, submenu_id: UUID, db: AsyncSession = Depends(get_async_session)):
    stmt = select(Submenu).filter(Submenu.id == submenu_id,  Submenu.menu_id == menu_id)
    submenu_from_db = (await db.execute(stmt)).scalar()
    if not submenu_from_db:
        if not submenu_from_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'submenu not found')
    return submenu_from_db


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=SubmenuResponse)
async def update_submenu(menu_id: UUID, submenu_id: UUID, submenu: MenuCreate, db: AsyncSession = Depends(get_async_session)):
    stmt1 = select(Submenu).filter(Submenu.id == submenu_id, Submenu.menu_id == menu_id)

    submenu_to_update = (await db.execute(stmt1)).scalar()

    if not submenu_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'submenu not found')

    stmt2 = update(Submenu).where(Submenu.menu_id == menu_id).values(title=submenu.title,
                                                                     description=submenu.description)
    await db.execute(stmt2)
    await db.commit()

    after_update = (await db.execute(stmt1)).scalar()
    return after_update


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
async def delete_menu(menu_id: UUID, submenu_id: UUID, db: AsyncSession = Depends(get_async_session)):
    stmt = delete(Submenu).filter(Submenu.id == submenu_id, Submenu.menu_id == menu_id)
    await db.execute(stmt)
    await db.commit()

    return {'detail': 'successfully deleted'}


##################
# Menu Endpoints #
##################


@app.post('/api/v1/menus', description='Create menus',
          status_code=status.HTTP_201_CREATED,
          response_model=MenuResponse)
async def create_menu(menu: MenuCreate, db: AsyncSession = Depends(get_async_session)):
    stmt = select(Menu).filter(Menu.title == menu.title)
    menu_from_db = (await db.execute(stmt)).scalar()

    if menu_from_db is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Menu with the title {menu.title} already exists in database')

    new_menu = Menu(**menu.model_dump())
    db.add(new_menu)
    await db.commit()
    await db.refresh(new_menu)
    return new_menu


@app.get('/api/v1/menus/{menu_id}', response_model=MenuResponse)
async def get_menu(menu_id: UUID, db: AsyncSession = Depends(get_async_session)):
    stmt = select(Menu).where(Menu.id == menu_id)
    menu_from_db = (await db.execute(stmt)).scalar()
    if not menu_from_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='menu not found')
    return menu_from_db


@app.get('/api/v1/menus', response_model=list[MenuResponse])
async def get_menu_list(db: AsyncSession = Depends(get_async_session)):
    stmt = select(Menu)
    result = await db.execute(stmt)
    menus = result.scalars()
    return menus


@app.delete('/api/v1/menus/{menu_id}')
async def delete_menu(menu_id: UUID, db: AsyncSession = Depends(get_async_session)):
    stmt = delete(Menu).filter(Menu.id == menu_id)
    await db.execute(stmt)
    await db.commit()

    return {'detail': 'successfully deleted'}


@app.patch('/api/v1/menus/{menu_id}', response_model=MenuResponse)
async def update_menu(menu_id: UUID, menu: MenuCreate, db: AsyncSession = Depends(get_async_session)):
    stmt1 = select(Menu).filter(Menu.id == menu_id)
    menu_to_update = (await db.execute(stmt1)).scalar()

    if not menu_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'menu not found')

    stmt2 = update(Menu).where(Menu.id == menu_id).values(title=menu.title,
                                                          description=menu.description)
    await db.execute(stmt2)
    await db.commit()

    after_update = (await db.execute(stmt1)).scalar()
    return after_update









