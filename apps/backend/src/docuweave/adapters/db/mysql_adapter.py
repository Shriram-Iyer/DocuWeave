"""
MySQL data adapter using aiomysql.
"""
from typing import Any
from urllib.parse import urlparse

import aiomysql  # type: ignore[import-untyped]

from docuweave.adapters.db.base_adapter import BaseDataAdapter


def _parse_dsn(dsn: str) -> dict[str, Any]:
    parsed = urlparse(dsn)
    return {
        "host": parsed.hostname or "localhost",
        "port": parsed.port or 3306,
        "user": parsed.username or "root",
        "password": parsed.password or "",
        "db": parsed.path.lstrip("/"),
        "autocommit": True,
        "cursorclass": aiomysql.DictCursor,
    }


class MySQLDataAdapter(BaseDataAdapter):
    def __init__(self, dsn: str) -> None:
        self._connect_kwargs = _parse_dsn(dsn)
        self._pool: aiomysql.Pool | None = None

    async def _get_pool(self) -> aiomysql.Pool:
        if self._pool is None:
            kwargs = {k: v for k, v in self._connect_kwargs.items() if k != "cursorclass"}
            self._pool = await aiomysql.create_pool(**kwargs)
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
            conditions = [f"`{col}` = %s" for col in filters]
            values = list(filters.values())
            where_clause = "WHERE " + " AND ".join(conditions)

        query = f"SELECT * FROM `{table}` {where_clause}"
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, values or None)
                rows = await cur.fetchall()
        return list(rows)

    async def list_tables(self) -> list[str]:
        pool = await self._get_pool()
        db_name = self._connect_kwargs["db"]
        query = "SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA = %s ORDER BY TABLE_NAME"
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, (db_name,))
                rows = await cur.fetchall()
        return [row["TABLE_NAME"] for row in rows]

    async def sample_table(self, table: str, limit: int = 10) -> list[dict[str, Any]]:
        return await self.fetch_table(table)  # simplified; add LIMIT in production

    async def close(self) -> None:
        if self._pool:
            self._pool.close()
            await self._pool.wait_closed()
            self._pool = None
