"""
Motor + Beanie initialization for MongoDB template DB.
"""
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from docuweave.config import settings


_client: AsyncIOMotorClient | None = None


async def init_mongo() -> None:
    """Call this once at app startup when TEMPLATE_DB_TYPE=mongodb."""
    global _client
    from docuweave.infrastructure.database.mongo.documents import (
        ComponentDocument,
        DataSourceDocument,
        LinkConfigDocument,
        TemplateDocument,
    )

    _client = AsyncIOMotorClient(settings.template_db_url)
    db_name = settings.template_db_url.split("/")[-1].split("?")[0] or "docuweave_templates"
    await init_beanie(
        database=_client[db_name],
        document_models=[TemplateDocument, ComponentDocument, DataSourceDocument, LinkConfigDocument],
    )


async def close_mongo() -> None:
    global _client
    if _client:
        _client.close()
        _client = None
