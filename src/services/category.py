"""Category service."""
from common.services.base import BaseCRUDService
from src.repositories.category import CategoryRepository


class CategoryService(BaseCRUDService):
    """Encapsulates Category logic."""

    def __init__(self, category_repository: CategoryRepository):
        """Initialize Category service."""
        super().__init__(category_repository)
        self._category_repo = category_repository
