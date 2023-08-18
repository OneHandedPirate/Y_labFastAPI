from typing import Any

from fastapi import Depends, HTTPException, status
from sqlalchemy import ScalarResult, String, cast, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Dish, Menu, Submenu
from app.db.session import get_async_session


class SQLAlchemyRepository:
    """Repository for async CRUD operations via SQLAlchemy"""

    model: Any = None
    related_model: Any = None
    related_model_field: Any = None

    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        self.session = session

    async def get(self, _id: int) -> ScalarResult:
        stmt = select(self.model).where(self.model.id == _id)
        obj = await self.session.scalar(stmt)
        await self.verify_existence(obj)
        return obj

    async def get_list(self, related_model_id: None | int = None) -> ScalarResult:
        if self.related_model is None:
            stmt = select(self.model)
        else:
            stmt = select(self.model).where(
                getattr(self.model, self.related_model_field) == related_model_id
            )
        objs = await self.session.scalars(stmt)
        return objs

    async def update(self, _id: int, data: dict) -> ScalarResult:
        stmt1 = select(self.model).where(self.model.id == _id)
        obj_to_update = await self.session.scalar(stmt1)

        await self.verify_existence(obj_to_update)

        stmt2 = update(self.model).where(self.model.id == _id).values(**data)

        await self.session.execute(stmt2)
        await self.session.commit()

        after_update = await self.session.scalar(stmt1)
        return after_update

    async def delete(self, _id: int) -> dict:
        stmt = select(self.model).where(self.model.id == _id)
        obj_to_delete = await self.session.scalar(stmt)
        await self.verify_existence(obj_to_delete)
        await self.session.delete(obj_to_delete)
        await self.session.commit()
        return {
            'detail': f'{self.model.__tablename__} with the id {_id} '
            f'successfully deleted'
        }

    async def create(self, data: dict, related_model_id: None | int = None) -> ScalarResult:
        stmt = select(self.model).filter(self.model.title == cast(data['title'], String))
        obj_from_db = await self.session.scalar(stmt)

        if obj_from_db is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'{self.model.__tablename__} with the '
                f'title {data["title"]} already exists in database',
            )
        if related_model_id:
            new_obj = self.model(**data, **{self.related_model_field: related_model_id})
        else:
            new_obj = self.model(**data)
        self.session.add(new_obj)
        await self.session.commit()
        await self.session.refresh(new_obj)
        return new_obj

    async def verify_existence(self, obj: ScalarResult | None) -> None:
        """Verifies object existence in database"""

        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'{self.model.__tablename__} not found',
            )


class MenuRepository(SQLAlchemyRepository):
    """Repo for CRUD operations with Menu objects"""

    model = Menu

    async def get_all(self) -> ScalarResult:
        stmt = select(self.model).options(selectinload(self.model.submenus).selectinload(Submenu.dishes))
        return await self.session.scalars(stmt)


class SubmenuRepository(SQLAlchemyRepository):
    """Repo for CRUD operations with Submenu objects"""

    model = Submenu
    related_model = Menu
    related_model_field = 'menu_id'


class DishRepository(SQLAlchemyRepository):
    """Repo for CRUD operations with Dish objects"""

    model = Dish
    related_model = Submenu
    related_model_field = 'submenu_id'
