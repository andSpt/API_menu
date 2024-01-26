from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator, UUID4


class BaseItem(BaseModel):
    title: str
    description: str


class MenuUpdate(BaseItem):
    title: str | None = None
    description: str | None = None


class MenuCreate(BaseItem):
    pass


class MenuResponse(BaseItem):
    id: UUID4
    submenus_count: int = 0
    dishes_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class SubmenuUpdate(BaseItem):
    title: str | None = None
    description: str | None = None


class SubmenuCreate(BaseItem):
    pass


class SubmenuResponse(BaseItem):
    id: UUID4
    dishes_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class DishCreate(BaseItem):
    price: Decimal


class DishUpdate(BaseItem):
    title: str | None = None
    description: str | None = None
    price: Decimal | None = None


class DishResponse(BaseItem):
    id: UUID4
    price: Decimal

    @field_validator('price')
    def round_price(cls, value) -> Decimal:
        result = Decimal(value).quantize(Decimal('.01'))
        return result

    model_config = ConfigDict(from_attributes=True)


