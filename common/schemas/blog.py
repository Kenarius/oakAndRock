from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from uuid import UUID


class BlogSchema(BaseModel):
    """Blog schema."""

    uuid: UUID
    created_at: datetime
    title: str
    first_media_url: str
    second_media_url: str
    paragraph: str
    description: str


class CreateBlogSchema(BaseModel):
    title: str
    paragraph: str
    description: str


class UpdateBlogSchema(BaseModel):
    title: Optional[str] = None
    paragraph: Optional[str] = None
    description: Optional[str] = None
