"""Catalog repository."""

from sqlalchemy.ext.asyncio import AsyncSession

from common.db.models.catalog import Catalog
from common.repositories.base import BaseRepository


class CatalogRepository(BaseRepository):
    """Catalog Repository."""

    model = Catalog

    def __init__(self, session: AsyncSession) -> None:
        """Init Repository session."""
        super().__init__(session)
