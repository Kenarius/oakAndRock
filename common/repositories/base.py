"""Module with base repository realization."""

import uuid
from typing import Any, Sequence, TypeVar, Union

from sqlalchemy import Row, RowMapping, select
from sqlalchemy.ext.asyncio import AsyncSession

from common.abstract.repository import IRepository
from common.core.exceptions.base import DBException
from common.db.base import Base

TableType = TypeVar("TableType", bound=Base)


class BaseRepository(IRepository):
    """Base Repository implementation."""

    model: TableType = None  # type: ignore

    def __init__(self, session: AsyncSession) -> None:
        """Initialize base repository with async session."""
        self._session = session

    async def list(self, filters: Union[tuple, None] = None) -> Sequence[Row | RowMapping | Any]:
        """Get list of filtered objects."""
        query = select(self.model).order_by(self.model.created_at)
        if filters is not None:
            query.filter(*filters)
        objects = await self._session.execute(query)
        return objects.scalars().all()

    async def retrieve(self, pk: uuid.UUID) -> Union[model, DBException]:
        """Get object by primary key."""
        res = await self._session.execute(select(self.model).where(self.model.uuid == pk))  # noqa
        obj = res.scalars().first()
        self.check_object(obj)    # noqa
        await self._session.refresh(obj)
        return obj
