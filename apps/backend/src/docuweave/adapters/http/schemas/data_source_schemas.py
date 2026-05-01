from datetime import datetime
from pydantic import BaseModel


class DataSourceCreateRequest(BaseModel):
    name: str
    db_type: str  # postgres | mysql | mongodb
    db_url: str


class DataSourceResponse(BaseModel):
    id: str
    name: str
    db_type: str
    created_at: datetime


class ConnectionTestResponse(BaseModel):
    connected: bool
    error: str | None = None
