from datetime import datetime
from decimal import Decimal
from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import UUID4, BaseModel, ConfigDict, EmailStr, field_validator, validator


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

    @field_validator("price")
    def round_price(cls, value) -> Decimal:
        result = Decimal(value).quantize(Decimal(".01"))
        return result

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    password: str
    email: EmailStr
    is_active: bool | None = True


class UserResponse(UserCreate):
    id: UUID4 | str
    password: bytes
    registered_at: datetime | None = datetime.utcnow()
    confirmation_token: str
    is_confirmed: bool

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)] | None = None
    password: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None


class TokenInfo(BaseModel):
    access_token: str
    token_type: str
