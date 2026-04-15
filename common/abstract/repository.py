"""Module with repository interface."""
from abc import ABC, abstractmethod
from typing import Any


class IRepository(ABC):
    """Repository interface class."""

    @abstractmethod
    async def list(self, *args: Any, **kwargs: Any) -> Any:
        """Get data from database."""
        raise NotImplementedError("Implement list method")
