"""
Build the correct data DB adapter based on DATA_DB_TYPE config.
"""
from docuweave.adapters.db.base_adapter import BaseDataAdapter
from docuweave.config import settings


def create_data_adapter(db_type: str | None = None, db_url: str | None = None) -> BaseDataAdapter:
    """
    Returns the correct BaseDataAdapter implementation.
    Uses settings defaults if parameters are not provided.
    """
    db_type = (db_type or settings.data_db_type).lower()
    db_url = db_url or settings.data_db_url

    if db_type == "postgres":
        from docuweave.adapters.db.postgres_adapter import PostgresDataAdapter
        return PostgresDataAdapter(db_url)
    elif db_type == "mysql":
        from docuweave.adapters.db.mysql_adapter import MySQLDataAdapter
        return MySQLDataAdapter(db_url)
    elif db_type == "mongodb":
        from docuweave.adapters.db.mongodb_adapter import MongoDBDataAdapter
        return MongoDBDataAdapter(db_url)
    else:
        raise ValueError(f"Unsupported DATA_DB_TYPE: '{db_type}'. Choose: postgres | mysql | mongodb")
