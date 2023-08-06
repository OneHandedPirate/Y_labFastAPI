from fastapi import APIRouter, Depends, status

from app.schemas.create import MenuCreate
from app.schemas.responses import MenuResponse
from app.services.handlers import MenuService

router = APIRouter(prefix='/api/v1/menus', tags=['Menu'])


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=MenuResponse,
)
async def create_menu(menu: MenuCreate, menu_service: MenuService = Depends()):
    """Create a new **menu**."""

    return await menu_service.create(menu.model_dump())


@router.get('/{menu_id}', response_model=MenuResponse)
async def get_menu(menu_id: int, menu_service: MenuService = Depends()):
    """Get a particular **menu** by its **ID**."""

    return await menu_service.get(menu_id)


@router.get('', response_model=list[MenuResponse])
async def get_menu_list(menu_service: MenuService = Depends()):
    """Get a list of **menus**."""

    return await menu_service.get_list()


@router.delete('/{menu_id}')
async def delete_menu(menu_id: int, menu_service: MenuService = Depends()):
    """Delete a particular **menu** by its **ID**."""

    return await menu_service.delete(menu_id)


@router.patch('/{menu_id}', response_model=MenuResponse)
async def update_menu(
    menu_id: int, menu: MenuCreate, menu_service: MenuService = Depends()
):
    """Update a particular **menu**."""

    return await menu_service.update(menu_id, menu.model_dump())
