import uuid

from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, select, func, cast
from sqlalchemy.orm import declarative_base, relationship, column_property
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class Dish(Base):
    __tablename__ = 'dish'

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)
    price = Column(Numeric(10, 2))
    submenu_id = Column(UUID, ForeignKey('submenu.id', ondelete='CASCADE'))

    submenu = relationship('Submenu', back_populates='dishes')


class Submenu(Base):
    __tablename__ = 'submenu'

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, unique=True)
    description = Column(String)
    menu_id = Column(UUID, ForeignKey('menu.id', ondelete='CASCADE'))

    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenu')

    dishes_count = column_property(
        select(func.count(Dish.id)).where(
            Dish.submenu_id == cast(id, UUID)).correlate_except(Dish).scalar_subquery()
    )


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, unique=True)
    description = Column(String)

    submenus = relationship('Submenu', back_populates='menu')

    submenus_count = column_property(
        select(func.count(Submenu.id)).where(
            Submenu.menu_id == cast(id, UUID)).correlate_except(Submenu).scalar_subquery()
    )

    dishes_count = column_property(
        select(func.count(Dish.id)).where(Dish.submenu_id.in_(
            select(Submenu.id).where(Submenu.menu_id == cast(id, UUID))
        )).correlate_except(Dish).scalar_subquery()
    )







