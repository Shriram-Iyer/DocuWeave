from fastapi import APIRouter, HTTPException

from docuweave.infrastructure.database.sql.engine import get_session
from docuweave.infrastructure.database.sql.models import DataSourceModel
from docuweave.infrastructure.adapter_factory import create_data_adapter
from docuweave.domain.entities.selector import SelectorConfig
from docuweave.use_cases.selectors.evaluate_selector import evaluate_selector
from docuweave.use_cases.selectors.get_selector_options import get_selector_options
from docuweave.adapters.http.schemas.selector_schemas import (
    SelectorOptionsRequest,
    SelectorEvaluateRequest,
)

router = APIRouter(prefix="/api/v1/selectors", tags=["selectors"])


async def _get_adapter_for(ds_id: str):  # type: ignore[return]
    async with get_session() as session:
        ds = await session.get(DataSourceModel, ds_id)
        if not ds:
            raise HTTPException(status_code=404, detail="Data source not found")
    return create_data_adapter(ds.db_type, ds.db_url), ds


@router.post("/options", response_model=list[dict])
async def selector_options(body: SelectorOptionsRequest) -> list[dict]:
    adapter, ds = await _get_adapter_for(body.data_source_id)
    try:
        rows = await adapter.fetch_table(body.selector_config.table, filters={})
    finally:
        await adapter.close()

    cfg = SelectorConfig(
        type=body.selector_config.type,
        table=body.selector_config.table,
        display_fields=body.selector_config.display_fields,
        multi_select=body.selector_config.multi_select,
    )
    return get_selector_options(rows, cfg)


@router.post("/evaluate", response_model=list[dict])
async def selector_evaluate(body: SelectorEvaluateRequest) -> list[dict]:
    adapter, ds = await _get_adapter_for(body.data_source_id)
    try:
        rows = await adapter.fetch_table(body.selector_config.table, filters={})
    finally:
        await adapter.close()

    cfg = SelectorConfig(
        type=body.selector_config.type,
        table=body.selector_config.table,
        display_fields=body.selector_config.display_fields,
        multi_select=body.selector_config.multi_select,
    )
    pk = cfg.display_fields[0] if cfg.display_fields else "id"
    return evaluate_selector(rows, cfg, body.selected_ids, pk_field=pk)
