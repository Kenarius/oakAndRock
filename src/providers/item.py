from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.item import ItemRepository
from src.services.item import ItemService


def provide_item_service(session: AsyncSession) -> ItemService:
    """Provide item service."""
    repository = ItemRepository(session)
    service = ItemService(repository)
    return service

