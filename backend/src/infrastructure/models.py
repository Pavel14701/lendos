from enum import Enum
from typing import Type

import sqlalchemy as sa
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    object_mapper,
    relationship,
)

from backend.src.infrastructure._types import DomainModel


class Base(DeclarativeBase):
    def to_domain(
        self, 
        dataclass: Type[DomainModel]
    ) -> DomainModel:
        """Mapping ORM model to dataclass"""
        data = {
            attr.key: getattr(self, attr.key)
            for attr in object_mapper(self).attrs
        }
        return dataclass(**data)


class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        sa.Integer, autoincrement=True, primary_key=True, index=True,
        comment="Unique user ID"
    )
    username: Mapped[str] = mapped_column(
        sa.String(length=255), unique=True, nullable=False, index=True, 
        comment="Unique username"
    )
    hashed_password: Mapped[str] = mapped_column(
        "hashed_password", sa.String(length=255), nullable=False,
        comment="Hashed user password"
    )
    salt: Mapped[str] = mapped_column(
        sa.String(length=16), nullable=False, 
        comment="Salt used for password hashing"
    )
    role: Mapped[UserRole] = mapped_column(
        sa.Enum(UserRole), nullable=False, default=UserRole.USER, 
        comment="User role (USER or ADMIN)"
    )