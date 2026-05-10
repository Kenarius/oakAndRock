"""Module with base repository realization."""

import uuid
from typing import Any, Sequence, TypeVar, Union

from sqlalchemy import Row, RowMapping, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.abstract.repository import IRepository
from common.core.exceptions.base import DBException
from common.db.base import Base, BaseModel

TableType = TypeVar("TableType", bound=Base)
CreateBaseSchema = TypeVar("CreateBaseSchema", bound=BaseModel)
UpdateBaseSchema = TypeVar("UpdateBaseSchema", bound=BaseModel)


class BaseRepository(IRepository):
    """Base Repository implementation."""

    model: TableType = None  # type: ignore
    create_scheme: CreateBaseSchema = None  # type: ignore
    update_scheme: UpdateBaseSchema = None  # type: ignore

    def __init__(self, session: AsyncSession) -> None:
        """Initialize base repository with async session."""
        self._session = session

    async def create(self, input_data: create_scheme) -> model:
        """Create model."""
        if hasattr(input_data, "model_dump"):
            values = input_data.model_dump()
        else:
            values = input_data
        obj = self.model(**values)   # noqa
        self._session.add(obj)
        await self._session.flush()
        await self._session.refresh(obj)
        return obj

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
        # self.check_object(obj)    # noqa
        await self._session.refresh(obj)
        return obj

    async def update(
            self, pk: uuid.UUID, input_data: update_scheme, partial: bool = True
    ) -> Union[model, DBException]:
        """Update object by specified primary key."""
        if hasattr(input_data, "model_dump"):
            values_dump_data = input_data.model_dump(exclude_unset=partial) # noqa
        else:
            values_dump_data = input_data
        if values_dump_data:
            updated_obj = await self._session.execute(
                update(self.model)
                .where(self.model.uuid == pk)   # noqa
                .values(**values_dump_data)
                .returning(self.model)
            )
            await self._session.flush()
            res = updated_obj.scalars().first()
            if res is None:
                raise DBException(
                    "Object Not Found",
                    status_code=404,
                    error_code="object_not_found",
                )
            await self._session.refresh(res)
            return res
        else:
            return await self._session.get(self.model, pk)

    async def delete(self, pk: uuid.UUID) -> dict:
        """Delete object by specified primary key."""
        res = await self._session.execute(delete(self.model).where(self.model.uuid == pk))  # noqa
        await self._session.flush()

        return {"affected_rows": res.rowcount}
