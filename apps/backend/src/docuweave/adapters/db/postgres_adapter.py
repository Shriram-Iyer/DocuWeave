"""
PostgreSQL data adapter using asyncpg.
"""
from typing import Any

import asyncpg  # type: ignore[import-untyped]

from docuweave.adapters.db.base_adapter import BaseDataAdapter


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
        where_clause = ""
        values: list[Any] = []

        if filters:
            conditions = []
            for i, (col, val) in enumerate(filters.items(), start=1):
                conditions.append(f"{col} = ${i}")
                values.append(val)
            where_clause = "WHERE " + " AND ".join(conditions)

        query = f'SELECT * FROM "{table}" {where_clause}'
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
        query = f'SELECT * FROM "{table}" LIMIT {limit}'
        async with pool.acquire() as conn:
            rows = await conn.fetch(query)
        return [dict(row) for row in rows]

    async def close(self) -> None:
        if self._pool:
            await self._pool.close()
            self._pool = None
