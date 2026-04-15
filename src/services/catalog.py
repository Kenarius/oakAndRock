"""Catalog service."""
from common.services.base import BaseCRUDService
from src.repositories.catalog import CatalogRepository


class CatalogService(BaseCRUDService):
    """Encapsulates Catalog logic."""

    def __init__(self, catalog_repository: CatalogRepository):
        """Initialize Catalog service."""
        super().__init__(catalog_repository)
        self._catalog_repo = catalog_repository
