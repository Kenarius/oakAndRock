from pydantic import BaseModel


class CatalogSchema(BaseModel):
    """Catalog schema."""

    title: str
    image_url: str
    pdf_url: str
