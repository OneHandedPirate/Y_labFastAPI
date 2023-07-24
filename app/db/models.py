from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, select, func, cast
from sqlalchemy.orm import declarative_base, relationship, column_property


Base = declarative_base()


class Dish(Base):
    __tablename__ = 'dish'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(Numeric(10, 2))
    submenu_id = Column(Integer, ForeignKey('submenu.id', ondelete='CASCADE'))

    submenu = relationship('Submenu', back_populates='dishes')


class Submenu(Base):
    __tablename__ = 'submenu'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    description = Column(String)
    menu_id = Column(Integer, ForeignKey('menu.id', ondelete='CASCADE'))

    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenu', cascade="all, delete")

    dishes_count = column_property(
        select(func.count(Dish.id)).where(
            Dish.submenu_id == cast(id, Integer)).correlate_except(Dish).scalar_subquery()
    )


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    description = Column(String)

    submenus = relationship('Submenu', back_populates='menu', cascade="all, delete")

    submenus_count = column_property(
        select(func.count(Submenu.id)).where(
            Submenu.menu_id == cast(id, Integer)).correlate_except(Submenu).scalar_subquery()
    )

    dishes_count = column_property(
        select(func.count(Dish.id)).where(Dish.submenu_id.in_(
            select(Submenu.id).where(Submenu.menu_id == cast(id, Integer))
        )).correlate_except(Dish).scalar_subquery()
    )
