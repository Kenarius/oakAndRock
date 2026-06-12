"""Catalog service."""
from common.core.utlis.images import upload_file_to_disk
from common.services.base import BaseCRUDService
from src.repositories.catalog import CatalogRepository


class CatalogService(BaseCRUDService):
    """Encapsulates Catalog logic."""

    def __init__(self, catalog_repository: CatalogRepository):
        """Initialize Catalog service."""
        super().__init__(catalog_repository)
        self._catalog_repo = catalog_repository

    async def create(self, data: dict):
        """Create obj."""
        pdf_url = None
        if data.get("pdf_file"):
            pdf_url = await upload_file_to_disk(data.get("pdf_file"), data["title"], "catalog_pdfs")

        image_url = None
        if data.get("image_file"):
            image_url = await upload_file_to_disk(data.get("image_file"), data["title"], "catalog_images")

        blog_data = {
            "title": data["title"],
            "image_url": image_url or "",
            "pdf_url": pdf_url or "",
        }
        obj = await self._repository.create(blog_data)
        return obj
