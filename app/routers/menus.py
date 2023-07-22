from fastapi import FastAPI, Depends, status, Response, HTTPException, APIRouter
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Menu, Submenu, Dish
from app.schemas import MenuCreate, MenuResponse
from app.db.session import get_async_session


router = APIRouter(prefix='/api/v1/menus')


@router.post('', description='Create menus', status_code=status.HTTP_201_CREATED,
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


@router.get('/{menu_id}', response_model=MenuResponse)
async def get_menu(menu_id: int, db: AsyncSession = Depends(get_async_session)):
    stmt = select(Menu).where(Menu.id == menu_id)
    menu_from_db = (await db.execute(stmt)).scalar()
    if not menu_from_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='menu not found')
    return menu_from_db


@router.get('', response_model=list[MenuResponse])
async def get_menu_list(db: AsyncSession = Depends(get_async_session)):
    stmt = select(Menu)
    result = await db.execute(stmt)
    menus = result.scalars()
    return menus


@router.delete('/{menu_id}')
async def delete_menu(menu_id: int, db: AsyncSession = Depends(get_async_session)):
    stmt = delete(Menu).filter(Menu.id == menu_id)
    await db.execute(stmt)
    await db.commit()

    return {'detail': 'successfully deleted'}


@router.patch('/{menu_id}', response_model=MenuResponse)
async def update_menu(menu_id: int, menu: MenuCreate, db: AsyncSession = Depends(get_async_session)):
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
