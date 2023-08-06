from fastapi import APIRouter, Depends, status

from app.schemas.create import DishCreate
from app.schemas.responses import DishResponse
from app.services.handlers import DishService

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['Dish']
)


@router.get('/{dish_id}', response_model=DishResponse)
async def get_dish(
    dish_id: int, dish_service: DishService = Depends()
):
    """Get a particular **dish** by its **ID**."""

    return await dish_service.get(dish_id)


@router.get('', response_model=list[DishResponse])
async def get_dishes_list(
    submenu_id: int, dish_service: DishService = Depends()
):
    """Get a list of dishes by **submenu** **ID**."""

    return await dish_service.get_list(submenu_id)


@router.post('', response_model=DishResponse,
             status_code=status.HTTP_201_CREATED)
async def create_dish(
    submenu_id: int,
    dish: DishCreate,
    dish_service: DishService = Depends(),
):
    """Create a new **dish**."""

    return await dish_service.create(dish.model_dump(), submenu_id)


@router.patch('/{dish_id}', response_model=DishResponse)
async def update_dish(
    dish_id: int,
    dish: DishCreate,
    dish_service: DishService = Depends(),
):
    """Update a particular **dish**."""

    return await dish_service.update(dish_id, dish.model_dump())


@router.delete('/{dish_id}')
async def delete_dish(dish_id: int, dish_service: DishService = Depends()):
    """Delete a particular **dish** by its **ID**."""

    return await dish_service.delete(dish_id)
