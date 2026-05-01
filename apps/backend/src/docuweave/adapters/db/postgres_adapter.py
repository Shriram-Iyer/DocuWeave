"""
PostgreSQL data adapter using asyncpg.
"""
import re
from typing import Any

import asyncpg  # type: ignore[import-untyped]

from docuweave.adapters.db.base_adapter import BaseDataAdapter

_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _safe_ident(name: str) -> str:
    """Raise ValueError if name is not a safe SQL identifier."""
    if not _IDENT_RE.match(name):
        raise ValueError(f"Invalid SQL identifier: {name!r}")
    return name


class PostgresDataAdapter(BaseDataAdapter):
    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._pool: asyncpg.Pool | None = None

    async def _get_pool(self) -> asyncpg.Pool:
        if self._pool is None:
            self._pool = await asyncpg.create_pool(self._dsn)
        return self._pool

    async def fetch_table(
        self,
        table: str,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        pool = await self._get_pool()
        safe_table = _safe_ident(table)
        where_clause = ""
        values: list[Any] = []

        if filters:
            conditions = []
            for i, (col, val) in enumerate(filters.items(), start=1):
                conditions.append(f'"{_safe_ident(col)}" = ${i}')
                values.append(val)
            where_clause = "WHERE " + " AND ".join(conditions)

        query = f'SELECT * FROM "{safe_table}" {where_clause}'
        async with pool.acquire() as conn:
            rows = await conn.fetch(query, *values)
        return [dict(row) for row in rows]

    async def list_tables(self) -> list[str]:
        pool = await self._get_pool()
        query = """
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """
        async with pool.acquire() as conn:
            rows = await conn.fetch(query)
        return [row["table_name"] for row in rows]

    async def sample_table(self, table: str, limit: int = 10) -> list[dict[str, Any]]:
        pool = await self._get_pool()
        safe_table = _safe_ident(table)
        query = f'SELECT * FROM "{safe_table}" LIMIT $1'
        async with pool.acquire() as conn:
            rows = await conn.fetch(query, limit)
        return [dict(row) for row in rows]

    async def close(self) -> None:
        if self._pool:
            await self._pool.close()
            self._pool = None
