from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_validator


class MenuCreate(BaseModel):
    title: str
    description: str


class MenuResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    submenus_count: int
    dishes_count: int


class SubmenuResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    dishes_count: int


class DishCreate(BaseModel):
    title: str
    description: str
    price: float


class DishResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    price: float

    @model_validator(mode='after')
    def convert_price(self):
        self.price = str(self.price)
        return self


