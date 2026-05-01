"""
Fetch multiple tables from the data DB concurrently using asyncio.gather.
No SQL joins are performed here — each table is fetched independently.
"""
import asyncio
from typing import Any, Protocol


class DataAdapter(Protocol):
    async def fetch_table(self, table: str, filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        ...


async def fetch_tables_parallel(
    adapter: DataAdapter,
    table_names: list[str],
    filters: dict[str, dict[str, Any]] | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """
    Fetch all tables concurrently.

    Args:
        adapter: The data DB adapter.
        table_names: List of table names to fetch.
        filters: Optional per-table filter dicts, keyed by table name.

    Returns:
        Dict mapping table name → list of row dicts.
    """
    if not table_names:
        return {}

    filters = filters or {}

    async def fetch_one(table: str) -> tuple[str, list[dict[str, Any]]]:
        rows = await adapter.fetch_table(table, filters.get(table))
        return table, rows

    results = await asyncio.gather(*[fetch_one(t) for t in table_names])
    return dict(results)
