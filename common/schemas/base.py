"""Base schema class for database models."""
from datetime import datetime
from types import UnionType
from typing import Union, get_args
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


class PydanticModel(BaseModel):
    """Base database class for handling int field with datatime meaning definition."""

    @field_validator("*", mode="before")
    @classmethod
    def datetime_transformator(cls, v, field):
        type_ = cls.__annotations__.get(field.field_name)
        if isinstance(type_, UnionType) and datetime in get_args(type_) and v is int:
            return datetime.fromtimestamp(v)
        return v

    model_config = ConfigDict(json_encoders={datetime: lambda dt: int(dt.timestamp())})


class BaseDB(PydanticModel):
    """Base database class definition."""

    uuid: Union[str, UUID]
    updated_at: datetime
    created_at: datetime


class OrderedItem(BaseModel):
    uuid: UUID
    position: int

    model_config = ConfigDict(from_attributes=True)
