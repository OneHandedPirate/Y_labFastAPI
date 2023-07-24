from fastapi import FastAPI

from app.routers.submenus import router as submenu_router
from app.routers.menus import router as menu_router
from app.routers.dishes import router as dishes_router


app = FastAPI(title='Cozy restaurant')


app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dishes_router)
