from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.catalog import CatalogRepository
from src.services.catalog import CatalogService


def provide_catalog_service(session: AsyncSession) -> CatalogService:
    """Provide admin events service."""
    repository = CatalogRepository(session)
    service = CatalogService(repository)
    return service
