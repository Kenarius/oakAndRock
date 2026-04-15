from pydantic import BaseModel
from uuid import UUID

from common.schemas.base import MarkSchema
from common.schemas.catalog import CatalogSchema
from common.schemas.item import ShortItemSchema


class ShortCategorySchema(BaseModel):
    """Short Category schema."""

    uuid: UUID
    title: str
    main_media_url: str


class DetailCategorySchema(BaseModel):
    """Detail Category schema."""

    uuid: UUID
    title: str
    paragraph: str
    description: str
    first_media_url: str
    second_media_url: str
    marks: list = []
    items: list[ShortItemSchema] = []


class CatalogsAndCategoriesResponse(BaseModel):
    categories: list[ShortCategorySchema]
    catalogs: list[CatalogSchema]
