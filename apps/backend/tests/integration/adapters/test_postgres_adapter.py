"""
Integration tests for the PostgreSQL data adapter.
Requires: docker compose -f docker-compose.test.yml up -d
"""
import pytest
from docuweave.adapters.db.postgres_adapter import PostgresAdapter
from tests.integration.conftest import TEST_PG_URL


@pytest.fixture
async def pg_adapter():
    adapter = PostgresAdapter(TEST_PG_URL)
    await adapter._ensure_pool()
    # Seed a test table
    async with adapter._pool.acquire() as conn:
        await conn.execute("DROP TABLE IF EXISTS integration_test_users")
        await conn.execute(
            "CREATE TABLE integration_test_users (user_id TEXT PRIMARY KEY, name TEXT, score INT)"
        )
        await conn.execute(
            "INSERT INTO integration_test_users VALUES ('u1', 'Alice', 90), ('u2', 'Bob', 80)"
        )
    yield adapter
    async with adapter._pool.acquire() as conn:
        await conn.execute("DROP TABLE IF EXISTS integration_test_users")
    await adapter.close()


@pytest.mark.integration
async def test_fetch_table_returns_rows(pg_adapter: PostgresAdapter) -> None:
    rows = await pg_adapter.fetch_table("integration_test_users", filters={})
    assert len(rows) == 2
    assert any(r["name"] == "Alice" for r in rows)


@pytest.mark.integration
async def test_list_tables_includes_test_table(pg_adapter: PostgresAdapter) -> None:
    tables = await pg_adapter.list_tables()
    assert "integration_test_users" in tables


@pytest.mark.integration
async def test_sample_table_respects_limit(pg_adapter: PostgresAdapter) -> None:
    rows = await pg_adapter.sample_table("integration_test_users", limit=1)
    assert len(rows) == 1


@pytest.mark.integration
async def test_fetch_with_filter(pg_adapter: PostgresAdapter) -> None:
    rows = await pg_adapter.fetch_table("integration_test_users", filters={"name": "Alice"})
    assert len(rows) == 1
    assert rows[0]["name"] == "Alice"
