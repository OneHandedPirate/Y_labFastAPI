from pydantic import BaseModel


class MenuCreate(BaseModel):
    """Schema for creating menu and submenu objects"""

    title: str
    description: str


class DishCreate(BaseModel):
    """Schema for creating dish objects"""

    title: str
    description: str
    price: float
