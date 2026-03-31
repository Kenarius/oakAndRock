"""Item service."""

from common.services.base import BaseCRUDService
from src.repositories.item import ItemRepository


class ItemService(BaseCRUDService):
    """Encapsulates Item logic."""

    def __init__(self, item_repository: ItemRepository):
        """Initialize Item service."""
        super().__init__(item_repository)
        self._item_repo = item_repository

