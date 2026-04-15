from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.blog import BlogRepository
from src.services.blog import BlogService


def provide_blog_service(session: AsyncSession) -> BlogService:
    """Provide admin events service."""
    repository = BlogRepository(session)
    service = BlogService(repository)
    return service
