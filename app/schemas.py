from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator, UUID4


class BaseItem(BaseModel):
    id: UUID4 | str | None = None
    title: str
    description: str

    
class MenuCreate(BaseItem):
    pass


class MenuOut(BaseItem):
    id: UUID4
    submenus_count: int
    dishes_count: int

    model_config = ConfigDict(from_attributes=True)


class SubmenuIn(BaseItem):
    pass


class SubmenuOut(BaseItem):
    id: UUID4
    dishes_count: int

    model_config = ConfigDict(from_attributes=True)


class DishIn(BaseItem):
    price: Decimal


class DishOut(BaseItem):
    id: UUID4
    price: Decimal

    @field_validator('price')
    def round_price(cls, value) -> Decimal:
        return Decimal(value).quantize(Decimal('.01'))

    model_config = ConfigDict(from_attributes=True)


