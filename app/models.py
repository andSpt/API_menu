import uuid
from typing import List

from sqlalchemy import ForeignKey, String, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, declared_attr
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}_table'


class Menu(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(50), index=True)
    description: Mapped[str] = mapped_column(String(125))

    submenus: Mapped[List["Submenu"]] = relationship(back_populates='menu', cascade="all, delete-orphan")


class Submenu(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(50), index=True)
    description: Mapped[str] = mapped_column(String(125))
    menu_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("menu_table.id", ondelete='CASCADE'))
    
    dishes: Mapped[List["Dish"]] = relationship(back_populates="submenu", cascade="all, delete-orphan")
    menu: Mapped["Menu"] = relationship(back_populates="submenus")


class Dish(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(50), index=True)
    description: Mapped[str] = mapped_column(String(125))
    price: Mapped[Numeric] = mapped_column(Numeric(precision=10, scale=2))
    submenu_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("submenu_table.id", ondelete='CASCADE'))

    submenu: Mapped["Submenu"] = relationship(back_populates="dishes")





