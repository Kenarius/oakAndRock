"""Category repository."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from common.db.models.category import Category
from common.repositories.base import BaseRepository


class CategoryRepository(BaseRepository):
    """Category Repository."""

    model = Category

    def __init__(self, session: AsyncSession) -> None:
        """Init Repository session."""
        super().__init__(session)

    async def retrieve(self, pk: uuid.UUID):
        res = await self._session.execute(
            select(self.model)
            .options(selectinload(Category.items))
            .where(self.model.uuid == pk)  # noqa
        )
        obj = res.scalars().first()
        self.check_object(obj)  # noqa
        return obj
