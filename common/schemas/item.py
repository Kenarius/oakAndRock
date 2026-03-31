from pydantic import BaseModel


class ShortItemSchema(BaseModel):
    """Short Item schema."""

    uuid: str
    title: str
    main_media_url: str
    subtitle: str
    price: str


class DetailItemSchema(BaseModel):
    """Detail Item schema."""

    uuid: str
    title: str
    paragraph: str
    description: str
    price: str
    media_urls: str
    description_marks: list
    marks: list
