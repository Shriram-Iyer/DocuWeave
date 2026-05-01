"""
SQLAlchemy async engine and session factory for the template DB (PostgreSQL or MySQL).
"""
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from docuweave.config import settings

# Adjust MySQL URL scheme to async driver
_url = settings.template_db_url
if _url.startswith("mysql://"):
    _url = _url.replace("mysql://", "mysql+aiomysql://", 1)

engine = create_async_engine(_url, echo=settings.debug, pool_pre_ping=True)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
