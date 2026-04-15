from pydantic import BaseModel


class CatalogSchema(BaseModel):
    """Catalog schema."""

    title: str
    image: str
    pdf_url: str
