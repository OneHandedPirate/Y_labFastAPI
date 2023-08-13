from fastapi import APIRouter, BackgroundTasks, Depends, status

from app.schemas.create import MenuCreate
from app.schemas.responses import MenuAllButIDResponse, MenuAllResponse, MenuResponse
from app.services.handlers import MenuService

router = APIRouter(prefix='/api/v1/menus', tags=['Menu'])


@router.get('/all_without_ids', response_model=list[MenuAllButIDResponse])
async def get_without_ids(menu_service: MenuService = Depends()):
    """Get all **menus** with **submenus** and **dishes** included without **ids**"""

    return await menu_service.get_all()


@router.get('/all', response_model=list[MenuAllResponse])
async def get_all(menu_service: MenuService = Depends()):
    """Get all **menus** with **submenus** and **dishes** included"""

    return await menu_service.get_all()


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=MenuResponse,
)
async def create_menu(menu: MenuCreate, bg_tasks: BackgroundTasks, menu_service: MenuService = Depends()):
    """Create a new **menu**."""

    return await menu_service.create(menu.model_dump(), bg_tasks=bg_tasks)


@router.get('/{menu_id}', response_model=MenuResponse)
async def get_menu(menu_id: int, menu_service: MenuService = Depends()):
    """Get a particular **menu** by its **ID**."""

    return await menu_service.get(menu_id)


@router.get('', response_model=list[MenuResponse])
async def get_menu_list(menu_service: MenuService = Depends()):
    """Get a list of **menus**."""

    return await menu_service.get_list()


@router.delete('/{menu_id}')
async def delete_menu(menu_id: int, bg_tasks: BackgroundTasks, menu_service: MenuService = Depends()):
    """Delete a particular **menu** by its **ID**."""

    return await menu_service.delete(menu_id, bg_tasks=bg_tasks)


@router.patch('/{menu_id}', response_model=MenuResponse)
async def update_menu(
    menu_id: int, menu: MenuCreate, bg_tasks: BackgroundTasks, menu_service: MenuService = Depends()
):
    """Update a particular **menu**."""

    return await menu_service.update(menu.model_dump(), menu_id, bg_tasks=bg_tasks)
