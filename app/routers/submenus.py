from fastapi import FastAPI, Depends, status, Response, HTTPException, APIRouter
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Menu, Submenu, Dish
from app.schemas import MenuCreate, MenuResponse, SubmenuResponse
from app.db.session import get_async_session


router = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus')


@router.post('', status_code=status.HTTP_201_CREATED,
             response_model=SubmenuResponse)
async def create_submenu(menu_id: int, submenu: MenuCreate, db: AsyncSession = Depends(get_async_session)):
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


@router.get('', response_model=list[SubmenuResponse])
async def get_submenu_list(menu_id: int, db: AsyncSession = Depends(get_async_session)):
    stmt = select(Submenu).filter(Submenu.menu_id == menu_id)
    submenu_list = (await db.execute(stmt)).scalars()
    return submenu_list


@router.get('/{submenu_id}', response_model=SubmenuResponse)
async def get_submenu(menu_id: int, submenu_id: int, db: AsyncSession = Depends(get_async_session)):
    stmt = select(Submenu).filter(Submenu.id == submenu_id,  Submenu.menu_id == menu_id)
    submenu_from_db = (await db.execute(stmt)).scalar()
    if not submenu_from_db:
        if not submenu_from_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'submenu not found')
    return submenu_from_db


@router.patch('/{submenu_id}', response_model=SubmenuResponse)
async def update_submenu(menu_id: int, submenu_id: int, submenu: MenuCreate, db: AsyncSession = Depends(get_async_session)):
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


@router.delete('/{submenu_id}')
async def delete_menu(menu_id: int, submenu_id: int, db: AsyncSession = Depends(get_async_session)):
    stmt = delete(Submenu).filter(Submenu.id == submenu_id, Submenu.menu_id == menu_id)
    await db.execute(stmt)
    await db.commit()

    return {'detail': 'successfully deleted'}
