from pydantic import BaseModel, ConfigDict, model_validator


class MenuCreate(BaseModel):
    title: str
    description: str


class DishCreate(BaseModel):
    title: str
    description: str
    price: float


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | str
    title: str
    description: str

    @model_validator(mode='after')
    def convert_id(self):
        self.id = str(self.id)
        return self


class MenuResponse(BaseResponse):
    submenus_count: int
    dishes_count: int


class SubmenuResponse(BaseResponse):
    dishes_count: int


class DishResponse(BaseResponse):
    price: float | str

    @model_validator(mode='after')
    def convert_price(self):
        self.price = str(self.price)
        return self
