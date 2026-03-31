from datetime import datetime

from pydantic import BaseModel

from common.schemas.item import ShortItemSchema


class ShortCategorySchema(BaseModel):
    """Short Category schema."""

    uuid: str
    title: str
    main_media_url: str
    created_at: datetime


class DetailCategorySchema(BaseModel):
    """Detail Category schema."""

    uuid: str
    title: str
    paragraph: str
    description: str
    first_media_url: str
    second_media_url: str
    marks: list
    items: list[ShortItemSchema] = []
