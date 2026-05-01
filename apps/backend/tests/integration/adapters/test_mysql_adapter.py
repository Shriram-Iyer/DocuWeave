"""
Integration tests for the MySQL data adapter.
Requires: docker compose -f docker-compose.test.yml up -d
"""
import pytest
from docuweave.adapters.db.mysql_adapter import MySQLAdapter
from tests.integration.conftest import TEST_MYSQL_URL


@pytest.fixture
async def mysql_adapter():
    adapter = MySQLAdapter(TEST_MYSQL_URL)
    await adapter._ensure_pool()
    async with adapter._pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DROP TABLE IF EXISTS integration_test_items")
            await cur.execute(
                "CREATE TABLE integration_test_items (item_id VARCHAR(50) PRIMARY KEY, label VARCHAR(100))"
            )
            await cur.execute(
                "INSERT INTO integration_test_items VALUES ('i1', 'Widget'), ('i2', 'Gadget')"
            )
        await conn.commit()
    yield adapter
    async with adapter._pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DROP TABLE IF EXISTS integration_test_items")
        await conn.commit()
    await adapter.close()


@pytest.mark.integration
async def test_fetch_table_returns_rows(mysql_adapter: MySQLAdapter) -> None:
    rows = await mysql_adapter.fetch_table("integration_test_items", filters={})
    assert len(rows) == 2
    assert any(r["label"] == "Widget" for r in rows)


@pytest.mark.integration
async def test_list_tables_includes_test_table(mysql_adapter: MySQLAdapter) -> None:
    tables = await mysql_adapter.list_tables()
    assert "integration_test_items" in tables
