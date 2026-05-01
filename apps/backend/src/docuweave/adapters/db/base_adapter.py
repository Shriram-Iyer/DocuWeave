"""
Abstract base class for all data DB adapters.

All concrete adapters (Postgres, MySQL, MongoDB) implement this interface.
Use cases depend only on this protocol — they never import a concrete adapter.
"""
from abc import ABC, abstractmethod
from typing import Any


class BaseDataAdapter(ABC):
    @abstractmethod
    async def fetch_table(
        self,
        table: str,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Fetch all rows from a table, optionally filtered.

        Args:
            table: Table (or collection) name.
            filters: Optional dict of {column: value} equality filters.

        Returns:
            List of row dicts. Each dict maps column name → value.
        """

    @abstractmethod
    async def list_tables(self) -> list[str]:
        """Return all available table names in the data DB."""

    @abstractmethod
    async def sample_table(self, table: str, limit: int = 10) -> list[dict[str, Any]]:
        """Return a sample of rows for schema discovery."""

    @abstractmethod
    async def close(self) -> None:
        """Release connection resources."""
