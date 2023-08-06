from fastapi import FastAPI

from app.core.settings import APP_DESC, TAGS_META
from app.routers.dishes import router as dishes_router
from app.routers.menus import router as menu_router
from app.routers.submenus import router as submenu_router

app = FastAPI(
    title='Restaurant API',
    summary='Little cozy restaurant API with some CRUD stuff.',
    description=APP_DESC,
    openapi_tags=TAGS_META
)


app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dishes_router)
