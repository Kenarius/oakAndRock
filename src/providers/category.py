from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.category import CategoryRepository
from src.services.category import CategoryService


def provide_category_service(session: AsyncSession) -> CategoryService:
    """Provide admin events service."""
    category_repository = CategoryRepository(session)
    service = CategoryService(category_repository=category_repository)
    return service
