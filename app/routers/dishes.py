from fastapi import APIRouter, Depends, status

from app.repositories.sqlalch import DishRepository
from app.schemas import DishCreate, DishResponse

router = APIRouter(
    prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["Dishes"]
)


@router.get("/{dish_id}", response_model=DishResponse)
async def get_dish(
    submenu_id: int, dish_id: int, dish_repo: DishRepository = Depends()
):
    return await dish_repo.get(dish_id, submenu_id)


@router.get("", response_model=list[DishResponse])
async def get_dishes_list(
    submenu_id: int, dish_repo: DishRepository = Depends()
):
    return await dish_repo.get_list(submenu_id)


@router.post("", response_model=DishResponse,
             status_code=status.HTTP_201_CREATED)
async def create_dish(
    submenu_id: int,
    dish: DishCreate,
    dish_repo: DishRepository = Depends(),
):
    return await dish_repo.create(dish.model_dump(), submenu_id)


@router.patch("/{dish_id}", response_model=DishResponse)
async def update_dish(
    dish_id: int,
    dish: DishCreate,
    dish_repo: DishRepository = Depends(),
):
    return await dish_repo.update(dish_id, dish.model_dump())


@router.delete("/{dish_id}")
async def delete_dish(dish_id: int, dish_repo: DishRepository = Depends()):
    return await dish_repo.delete(dish_id)
