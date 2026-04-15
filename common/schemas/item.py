from pydantic import BaseModel
from uuid import UUID

from common.schemas.base import MarkSchema


class DescriptionMarkSchema(BaseModel):
    """Description mark schema."""

    title: str
    subtitle: str


class ShortItemSchema(BaseModel):
    """Short Item schema."""

    uuid: UUID
    title: str
    main_media_url: str
    subtitle: str
    price: str


class DetailItemSchema(BaseModel):
    """Detail Item schema."""

    uuid: UUID
    title: str
    paragraph: str
    description: str
    price: str
    media_urls: str
    description_marks: list
    marks: list
