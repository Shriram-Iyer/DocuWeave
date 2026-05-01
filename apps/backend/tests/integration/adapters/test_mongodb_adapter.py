"""
Integration tests for the MongoDB data adapter.
Requires: docker compose -f docker-compose.test.yml up -d
"""
import pytest
from docuweave.adapters.db.mongodb_adapter import MongoDBAdapter
from tests.integration.conftest import TEST_MONGO_URL


@pytest.fixture
async def mongo_adapter():
    adapter = MongoDBAdapter(TEST_MONGO_URL)
    db = adapter._client.get_default_database()
    await db["int_test_products"].drop()
    await db["int_test_products"].insert_many([
        {"product_id": "p1", "title": "Alpha"},
        {"product_id": "p2", "title": "Beta"},
    ])
    yield adapter
    await db["int_test_products"].drop()
    await adapter.close()


@pytest.mark.integration
async def test_fetch_collection_returns_docs(mongo_adapter: MongoDBAdapter) -> None:
    rows = await mongo_adapter.fetch_table("int_test_products", filters={})
    assert len(rows) == 2
    assert "_id" not in rows[0]


@pytest.mark.integration
async def test_list_tables_includes_collection(mongo_adapter: MongoDBAdapter) -> None:
    tables = await mongo_adapter.list_tables()
    assert "int_test_products" in tables
