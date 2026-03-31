"""Base CRUD Service realizations."""
import uuid as _uuid
from typing import TypeVar

from common.abstract.repository import IRepository
from common.abstract.service import ICRUDService
from common.db import BaseModel

ServiceRepository = TypeVar("ServiceRepository", bound=IRepository)


class BaseCRUDService(ICRUDService):
    """Base CRUD Service realization."""

    def __init__(self, repository: ServiceRepository) -> None:
        """Init method of base crud service class."""
        self._repository = repository

    async def get_by_uuid(self, uuid: _uuid.UUID):
        """Get obj by uuid."""
        obj = await self._repository.retrieve(uuid)
        return obj

    async def get_all(self):
        """Get all objects."""
        objs = await self._repository.list()
        return objs