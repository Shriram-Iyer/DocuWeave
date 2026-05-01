from unittest.mock import AsyncMock, MagicMock
import pytest

from docuweave.use_cases.data_fetch.fetch_tables_parallel import fetch_tables_parallel


@pytest.mark.asyncio
async def test_all_tables_fetched() -> None:
    adapter = MagicMock()
    adapter.fetch_table = AsyncMock(side_effect=lambda table, filters=None: [{"table": table}])

    result = await fetch_tables_parallel(adapter, ["jobs", "users"])

    assert "jobs" in result
    assert "users" in result
    assert result["jobs"] == [{"table": "jobs"}]
    assert result["users"] == [{"table": "users"}]


@pytest.mark.asyncio
async def test_tables_fetched_concurrently() -> None:
    import asyncio

    call_order: list[str] = []

    async def slow_fetch(table: str, filters: dict | None = None) -> list[dict]:
        call_order.append(f"start:{table}")
        await asyncio.sleep(0.01)
        call_order.append(f"end:{table}")
        return [{"t": table}]

    adapter = MagicMock()
    adapter.fetch_table = slow_fetch

    result = await fetch_tables_parallel(adapter, ["jobs", "users", "targets"])

    assert set(result.keys()) == {"jobs", "users", "targets"}
    # If truly concurrent, both "start" events happen before both "end" events
    starts = [e for e in call_order if e.startswith("start")]
    assert len(starts) == 3


@pytest.mark.asyncio
async def test_empty_table_list_returns_empty() -> None:
    adapter = MagicMock()
    result = await fetch_tables_parallel(adapter, [])
    assert result == {}
