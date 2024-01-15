from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator, UUID4


class BaseItem(BaseModel):
    title: str
    description: str

    
class MenuCreateSchema(BaseItem):
    id: UUID4 | str | None = None


class MenuUpdateSchema(MenuCreateSchema):
    title: str | None = None
    description: str | None = None


class MenuSchema(MenuCreateSchema):
    id: UUID4
    submenus_count: int
    dishes_count: int

    model_config = ConfigDict(from_attributes=True)





class SubmenuCreate(BaseItem):
    pass


class Submenu(SubmenuCreate):
    id: UUID4
    dishes_count: int

    model_config = ConfigDict(from_attributes=True)


class SubmenuUpdatePartial(SubmenuCreate):
    title: str | None = None
    description: str | None = None


class DishCreate(BaseItem):
    price: Decimal


class Dish(BaseItem):
    id: UUID4
    price: Decimal

    @field_validator('price')
    def round_price(cls, value) -> Decimal:
        return Decimal(value).quantize(Decimal('.01'))

    model_config = ConfigDict(from_attributes=True)


class DishUpdatePartial(DishCreate):
    title: str | None = None
    description: str | None = None
    price: Decimal | None = None


