from pydantic import BaseModel, ConfigDict, model_validator


class MenuCreate(BaseModel):
    """Schema for creating menu and submenu objects"""

    title: str
    description: str


class DishCreate(BaseModel):
    """Schema for creating dish objects"""

    title: str
    description: str
    price: float


class BaseResponse(BaseModel):
    """Base schema for response"""

    model_config = ConfigDict(from_attributes=True)

    id: int | str
    title: str
    description: str

    @model_validator(mode="after")
    def convert_id(self):
        """Converts id field to a string"""

        self.id = str(self.id)
        return self


class MenuResponse(BaseResponse):
    """Menu Response schema"""

    submenus_count: int
    dishes_count: int


class SubmenuResponse(BaseResponse):
    """Submenu Response schema"""

    dishes_count: int


class DishResponse(BaseResponse):
    """Dish response schema"""

    price: float | str

    @model_validator(mode="after")
    def convert_price(self):
        """Converts price value to a string"""

        self.price = f"{self.price:.2f}"
        return self
