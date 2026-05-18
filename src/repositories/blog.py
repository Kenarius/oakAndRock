"""Blog repository."""
from typing import Union, Sequence, Any

from sqlalchemy import Row, RowMapping, select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from common.db.models.blog import Blog
from common.repositories.base import BaseRepository


class BlogRepository(BaseRepository):
    """Blog Repository."""

    model = Blog

    def __init__(self, session: AsyncSession) -> None:
        """Init Repository session."""
        super().__init__(session)
