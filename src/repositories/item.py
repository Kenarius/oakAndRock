"""Item repository."""

from sqlalchemy.ext.asyncio import AsyncSession

from common.db.models.item import Item
from common.repositories.base import BaseRepository


class ItemRepository(BaseRepository):
    """Item Repository."""

    model = Item

    def __init__(self, session: AsyncSession) -> None:
        """Init Repository session."""
        super().__init__(session)

