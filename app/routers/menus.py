from fastapi import Depends, status, APIRouter

from app.repositories.sqlalch import MenuRepository
from app.schemas import MenuCreate, MenuResponse


router = APIRouter(prefix='/api/v1/menus', tags=['Menu'])


@router.post('', description='Create menus', status_code=status.HTTP_201_CREATED,
             response_model=MenuResponse)
async def create_menu(menu: MenuCreate, menu_repo: MenuRepository = Depends()):
    return await menu_repo.create(menu.model_dump())


@router.get('/{menu_id}', response_model=MenuResponse)
async def get_menu(menu_id: int, menu_repo: MenuRepository = Depends()):
    return await menu_repo.get(menu_id)


@router.get('', response_model=list[MenuResponse])
async def get_menu_list(menu_repo: MenuRepository = Depends()):
    return await menu_repo.get_list()


@router.delete('/{menu_id}')
async def delete_menu(menu_id: int, menu_repo: MenuRepository = Depends()):
    return await menu_repo.delete(menu_id)


@router.patch('/{menu_id}', response_model=MenuResponse)
async def update_menu(menu_id: int, menu: MenuCreate,
                      menu_repo: MenuRepository = Depends()):
    return await menu_repo.update(menu_id, menu.model_dump())
