"""Module with CRUD Service interface."""
from abc import ABC, abstractmethod
from typing import Any


class ICRUDService(ABC):
    """CRUD Service interface."""

    @abstractmethod
    async def get_all(self, *args, **kwargs) -> Any:
        """Get obj by uuid."""
        raise NotImplementedError("Implement get_all method")
