from datetime import datetime

from pydantic import BaseModel


class BlogSchema(BaseModel):
    """Blog schema."""

    created_at: datetime
    title: str
    first_media_url: str
    second_media_url: str
    paragraph: str
    description: str
