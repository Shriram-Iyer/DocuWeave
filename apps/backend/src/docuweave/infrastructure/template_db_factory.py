"""
Determine which template DB backend to initialize at startup
based on TEMPLATE_DB_TYPE config.

Usage in main.py lifespan:
    await init_template_db()
"""
from docuweave.config import settings


async def init_template_db() -> None:
    db_type = settings.template_db_type.lower()

    if db_type in ("postgres", "mysql"):
        from sqlalchemy.ext.asyncio import create_async_engine
        from docuweave.infrastructure.database.sql.models import Base
        url = settings.template_db_url
        if url.startswith("mysql://"):
            url = url.replace("mysql://", "mysql+aiomysql://", 1)
        engine = create_async_engine(url)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        await engine.dispose()

    elif db_type == "mongodb":
        from docuweave.infrastructure.database.mongo.connection import init_mongo
        await init_mongo()

    else:
        raise ValueError(
            f"Unsupported TEMPLATE_DB_TYPE: '{db_type}'. Choose: postgres | mysql | mongodb"
        )


async def close_template_db() -> None:
    db_type = settings.template_db_type.lower()
    if db_type == "mongodb":
        from docuweave.infrastructure.database.mongo.connection import close_mongo
        await close_mongo()
