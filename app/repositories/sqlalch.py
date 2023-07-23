from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from app.db.models import Menu, Submenu, Dish
from app.repositories.base import BaseCRUDRepository
from app.db.session import get_async_session


class SQLAlchemyRepository(BaseCRUDRepository):
    model = None
    related_model = None
    related_model_field = None

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def get(self, *args):
        if self.related_model is None:
            stmt = select(self.model).where(self.model.id == args[0])
        else:
            stmt = select(self.model).where(self.model.id == args[0],
                getattr(self.model, self.related_model_field) == args[1])
        obj = await self.session.scalar(stmt)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'{self.model.__tablename__} not found')
        return obj

    async def get_list(self, *args):
        if self.related_model is None:
            stmt = select(self.model)
        else:
            stmt = select(self.model).where(
                getattr(self.model, self.related_model_field) == args[0])
        objs = await self.session.scalars(stmt)
        return objs

    async def update(self, _id, data):
        stmt1 = select(self.model).where(self.model.id == _id)
        obj_to_update = await self.session.scalar(stmt1)

        if not obj_to_update:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'{self.model.__tablename__} not found')

        stmt2 = update(self.model).where(self.model.id == _id).values(**data)

        await self.session.execute(stmt2)
        await self.session.commit()

        after_update = await self.session.scalar(stmt1)
        return after_update

    async def delete(self, _id):
        stmt = delete(self.model).where(self.model.id == _id)
        await self.session.execute(stmt)
        await self.session.commit()
        return {'detail': 'successfully deleted'}

    async def create(self, data, *args):
        stmt = select(self.model).filter(self.model.title == data['title'])
        obj_from_db = await self.session.scalar(stmt)

        if obj_from_db is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'{self.model.__tablename__} with the '
                                       f'title {data["title"]} already exists in database')
        if args:
            new_obj = self.model(**data, **{self.related_model_field: args[0]})
        else:
            new_obj = self.model(**data)
        self.session.add(new_obj)
        await self.session.commit()
        await self.session.refresh(new_obj)
        return new_obj


class MenuRepository(SQLAlchemyRepository):
    model = Menu


class SubmenuRepository(SQLAlchemyRepository):
    model = Submenu
    related_model = Menu
    related_model_field = 'menu_id'


class DishRepository(SQLAlchemyRepository):
    model = Dish
    related_model = Submenu
    related_model_field = 'submenu_id'
