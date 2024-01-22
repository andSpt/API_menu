from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator, UUID4


class BaseItem(BaseModel):
    title: str
    description: str

    
class MenuCreate(BaseItem):
    pass


class MenuUpdate(MenuCreate):
    pass


class MenuResponse(MenuCreate):
    id: UUID4
    submenus_count: int = 0
    dishes_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class SubmenuCreate(BaseItem):
    pass


class SubmenuUpdate(SubmenuCreate):
    pass


class SubmenuResponse(SubmenuCreate):
    dishes_count: int

    model_config = ConfigDict(from_attributes=True)


class DishCreate(BaseItem):
    price: Decimal

class DishUpdate(DishCreate):
    title: str
    price: Decimal


class DishResponse(DishCreate):
    id: UUID4
    price: Decimal

    @field_validator('price')
    def round_price(cls, value) -> Decimal:
        return Decimal(value).quantize(Decimal('.01'))

    model_config = ConfigDict(from_attributes=True)


