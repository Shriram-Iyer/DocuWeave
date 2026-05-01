"""
Integration test: template CRUD against a real PostgreSQL template DB.
Requires: docker compose -f docker-compose.test.yml up -d
Set TEMPLATE_DB_URL=postgresql+asyncpg://docuweave:docuweave@localhost:15432/docuweave_test
"""
import os
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select

from docuweave.infrastructure.database.sql.models import Base, TemplateModel


TEST_DB_URL = os.getenv(
    "TEST_PG_URL",
    "postgresql+asyncpg://docuweave:docuweave@localhost:15432/docuweave_test",
)


@pytest.fixture(scope="module")
async def test_engine():
    engine = create_async_engine(TEST_DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def session(test_engine):
    factory = async_sessionmaker(test_engine, expire_on_commit=False)
    async with factory() as s:
        yield s
        await s.rollback()


@pytest.mark.integration
async def test_create_and_retrieve_template(session: AsyncSession) -> None:
    t = TemplateModel(id="tpl-int-1", name="Integration Template", output_format="docx")
    session.add(t)
    await session.commit()

    result = await session.execute(select(TemplateModel).where(TemplateModel.id == "tpl-int-1"))
    fetched = result.scalar_one_or_none()
    assert fetched is not None
    assert fetched.name == "Integration Template"


@pytest.mark.integration
async def test_delete_template(session: AsyncSession) -> None:
    t = TemplateModel(id="tpl-int-del", name="To Delete", output_format="xlsx")
    session.add(t)
    await session.commit()
    await session.delete(t)
    await session.commit()

    result = await session.execute(select(TemplateModel).where(TemplateModel.id == "tpl-int-del"))
    assert result.scalar_one_or_none() is None
