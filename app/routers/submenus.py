from fastapi import Depends, APIRouter, status

from app.repositories.sqlalch import SubmenuRepository
from app.schemas import SubmenuResponse, MenuCreate


router = APIRouter(prefix='/api/v1/menus/{menu_id}/submenus', tags=['Submenu'])


@router.post('', status_code=status.HTTP_201_CREATED,
             response_model=SubmenuResponse)
async def create_submenu(menu_id: int, submenu: MenuCreate,
                         submenu_repo: SubmenuRepository = Depends()):
    return await submenu_repo.create(submenu.model_dump(), menu_id)


@router.get('', response_model=list[SubmenuResponse])
async def get_submenu_list(menu_id: int,
                           submenu_repo: SubmenuRepository = Depends()):
    submenus = await submenu_repo.get_list(menu_id)
    return submenus


@router.get('/{submenu_id}', response_model=SubmenuResponse)
async def get_submenu(menu_id: int, submenu_id: int,
                      submenu_repo: SubmenuRepository = Depends()):
    return await submenu_repo.get(submenu_id, menu_id)


@router.patch('/{submenu_id}', response_model=SubmenuResponse)
async def update_submenu(menu_id: int, submenu_id: int, submenu: MenuCreate,
                         submenu_repo: SubmenuRepository = Depends()):
    return await submenu_repo.update(submenu_id, submenu.model_dump())


@router.delete('/{submenu_id}')
async def delete_menu(submenu_id: int,
                      submenu_repo: SubmenuRepository = Depends()):
    return await submenu_repo.delete(submenu_id)
