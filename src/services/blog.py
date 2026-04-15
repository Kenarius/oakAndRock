"""Blog service."""
from common.services.base import BaseCRUDService
from src.repositories.blog import BlogRepository


class BlogService(BaseCRUDService):
    """Encapsulates Blog logic."""

    def __init__(self, blog_repository: BlogRepository):
        """Initialize Blog service."""
        super().__init__(blog_repository)
        self._blog_repo = blog_repository
