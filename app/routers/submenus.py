from fastapi import APIRouter, Depends, status

from app.schemas import MenuCreate, SubmenuResponse
from app.services.menu import SubmenuService

router = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus', tags=['Submenu'])


@router.post('', status_code=status.HTTP_201_CREATED,
             response_model=SubmenuResponse)
async def create_submenu(menu_id: int, submenu: MenuCreate,
                         submenu_service: SubmenuService = Depends()):
    return await submenu_service.create(submenu.model_dump(), menu_id)


@router.get('', response_model=list[SubmenuResponse])
async def get_submenu_list(menu_id: int,
                           submenu_service: SubmenuService = Depends()):
    submenus = await submenu_service.get_list(menu_id)
    return submenus


@router.get('/{submenu_id}', response_model=SubmenuResponse)
async def get_submenu(
    submenu_id: int, submenu_service: SubmenuService = Depends()
):
    return await submenu_service.get(submenu_id)


@router.patch('/{submenu_id}', response_model=SubmenuResponse)
async def update_submenu(
    submenu_id: int,
    submenu: MenuCreate,
    submenu_service: SubmenuService = Depends(),
):
    return await submenu_service.update(submenu_id, submenu.model_dump())


@router.delete('/{submenu_id}')
async def delete_menu(submenu_id: int,
                      submenu_service: SubmenuService = Depends()):
    return await submenu_service.delete(submenu_id)
