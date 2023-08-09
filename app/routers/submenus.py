from fastapi import APIRouter, Depends, status

from app.schemas.create import MenuCreate
from app.schemas.responses import SubmenuResponse
from app.services.handlers import SubmenuService

router = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus', tags=['Submenu'])


@router.post('', status_code=status.HTTP_201_CREATED,
             response_model=SubmenuResponse)
async def create_submenu(menu_id: int, submenu: MenuCreate,
                         submenu_service: SubmenuService = Depends()):
    """Create a new **submenu**."""

    return await submenu_service.create(submenu.model_dump(), menu_id)


@router.get('', response_model=list[SubmenuResponse])
async def get_submenu_list(menu_id: int,
                           submenu_service: SubmenuService = Depends()):
    """Get a list of **submenu** by **menu ID**."""

    return await submenu_service.get_list(menu_id)


@router.get('/{submenu_id}', response_model=SubmenuResponse)
async def get_submenu(
    menu_id: int, submenu_id: int, submenu_service: SubmenuService = Depends()
):
    """Get a particular **submenu** by its **ID**."""

    return await submenu_service.get(menu_id, submenu_id)


@router.patch('/{submenu_id}', response_model=SubmenuResponse)
async def update_submenu(
    menu_id: int,
    submenu_id: int,
    submenu: MenuCreate,
    submenu_service: SubmenuService = Depends(),
):
    """Update a particular **submenu**."""

    return await submenu_service.update(submenu.model_dump(), menu_id, submenu_id)


@router.delete('/{submenu_id}')
async def delete_menu(
        menu_id: int,
        submenu_id: int,
        submenu_service: SubmenuService = Depends()
):
    """Delete a particular **submenu** by its **ID**."""

    return await submenu_service.delete(menu_id, submenu_id)
