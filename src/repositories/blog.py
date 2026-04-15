"""Blog repository."""

from sqlalchemy.ext.asyncio import AsyncSession

from common.db.models.blog import Blog
from common.repositories.base import BaseRepository


class BlogRepository(BaseRepository):
    """Blog Repository."""

    model = Blog

    def __init__(self, session: AsyncSession) -> None:
        """Init Repository session."""
        super().__init__(session)
