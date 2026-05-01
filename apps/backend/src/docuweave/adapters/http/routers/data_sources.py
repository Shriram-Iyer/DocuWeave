import uuid

from fastapi import APIRouter, HTTPException, status

from docuweave.infrastructure.database.sql.engine import get_session
from docuweave.infrastructure.database.sql.models import DataSourceModel
from docuweave.infrastructure.adapter_factory import create_data_adapter
from docuweave.adapters.http.schemas.data_source_schemas import (
    DataSourceCreateRequest,
    DataSourceResponse,
    ConnectionTestResponse,
)
from sqlalchemy import select

router = APIRouter(prefix="/api/v1/data-sources", tags=["data-sources"])


def _to_response(ds: DataSourceModel) -> DataSourceResponse:
    return DataSourceResponse(
        id=ds.id,
        name=ds.name,
        db_type=ds.db_type,
        created_at=ds.created_at,
    )


@router.get("", response_model=list[DataSourceResponse])
async def list_data_sources() -> list[DataSourceResponse]:
    async with get_session() as session:
        result = await session.execute(select(DataSourceModel))
        return [_to_response(ds) for ds in result.scalars().all()]


@router.post("", response_model=DataSourceResponse, status_code=status.HTTP_201_CREATED)
async def create_data_source(body: DataSourceCreateRequest) -> DataSourceResponse:
    async with get_session() as session:
        ds = DataSourceModel(
            id=str(uuid.uuid4()),
            name=body.name,
            db_type=body.db_type,
            db_url=body.db_url,
        )
        session.add(ds)
        await session.commit()
        await session.refresh(ds)
        return _to_response(ds)


@router.get("/{ds_id}", response_model=DataSourceResponse)
async def get_data_source(ds_id: str) -> DataSourceResponse:
    async with get_session() as session:
        ds = await session.get(DataSourceModel, ds_id)
        if not ds:
            raise HTTPException(status_code=404, detail="Data source not found")
        return _to_response(ds)


@router.put("/{ds_id}", response_model=DataSourceResponse)
async def update_data_source(ds_id: str, body: DataSourceCreateRequest) -> DataSourceResponse:
    async with get_session() as session:
        ds = await session.get(DataSourceModel, ds_id)
        if not ds:
            raise HTTPException(status_code=404, detail="Data source not found")
        ds.name = body.name
        ds.db_type = body.db_type
        ds.db_url = body.db_url
        await session.commit()
        await session.refresh(ds)
        return _to_response(ds)


@router.delete("/{ds_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_data_source(ds_id: str) -> None:
    async with get_session() as session:
        ds = await session.get(DataSourceModel, ds_id)
        if not ds:
            raise HTTPException(status_code=404, detail="Data source not found")
        await session.delete(ds)
        await session.commit()


@router.post("/{ds_id}/test", response_model=ConnectionTestResponse)
async def test_connection(ds_id: str) -> ConnectionTestResponse:
    async with get_session() as session:
        ds = await session.get(DataSourceModel, ds_id)
        if not ds:
            raise HTTPException(status_code=404, detail="Data source not found")

    adapter = create_data_adapter(ds.db_type, ds.db_url)
    try:
        await adapter.list_tables()
        return ConnectionTestResponse(connected=True)
    except Exception as exc:
        return ConnectionTestResponse(connected=False, error=str(exc))
    finally:
        await adapter.close()


@router.get("/{ds_id}/tables", response_model=list[str])
async def list_tables(ds_id: str) -> list[str]:
    async with get_session() as session:
        ds = await session.get(DataSourceModel, ds_id)
        if not ds:
            raise HTTPException(status_code=404, detail="Data source not found")

    adapter = create_data_adapter(ds.db_type, ds.db_url)
    try:
        return await adapter.list_tables()
    finally:
        await adapter.close()


@router.get("/{ds_id}/tables/{table}/sample", response_model=list[dict])
async def sample_table(ds_id: str, table: str) -> list[dict]:
    async with get_session() as session:
        ds = await session.get(DataSourceModel, ds_id)
        if not ds:
            raise HTTPException(status_code=404, detail="Data source not found")

    adapter = create_data_adapter(ds.db_type, ds.db_url)
    try:
        return await adapter.sample_table(table, limit=10)
    finally:
        await adapter.close()
