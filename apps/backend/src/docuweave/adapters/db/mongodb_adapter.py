"""
MongoDB data adapter using motor (async).
"""
from typing import Any
from urllib.parse import urlparse

import motor.motor_asyncio  # type: ignore[import-untyped]

from docuweave.adapters.db.base_adapter import BaseDataAdapter


class MongoDBDataAdapter(BaseDataAdapter):
    def __init__(self, dsn: str) -> None:
        parsed = urlparse(dsn)
        self._db_name = parsed.path.lstrip("/") or "docuweave_data"
        self._client: motor.motor_asyncio.AsyncIOMotorClient = motor.motor_asyncio.AsyncIOMotorClient(dsn)
        self._db = self._client[self._db_name]

    async def fetch_table(
        self,
        table: str,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        query = filters or {}
        cursor = self._db[table].find(query, {"_id": 0})
        return await cursor.to_list(length=None)

    async def list_tables(self) -> list[str]:
        return await self._db.list_collection_names()

    async def sample_table(self, table: str, limit: int = 10) -> list[dict[str, Any]]:
        cursor = self._db[table].find({}, {"_id": 0}).limit(limit)
        return await cursor.to_list(length=limit)

    async def close(self) -> None:
        self._client.close()
