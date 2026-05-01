from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from docuweave.infrastructure.database.sql.engine import get_session
from docuweave.infrastructure.database.sql.models import DataSourceModel, TemplateModel, LinkConfigModel
from docuweave.infrastructure.adapter_factory import create_data_adapter
from docuweave.domain.entities.template import Template, TemplateComponent
from docuweave.domain.entities.table_link import LinkConfig, TableConfig, LinkDef
from docuweave.use_cases.document_generation.generate_document import generate_document
from docuweave.adapters.http.schemas.document_schemas import GenerateDocumentRequest

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


def _build_template(tm: TemplateModel) -> Template:
    components = [
        TemplateComponent(
            id=c.id,
            template_id=c.template_id,
            type=c.type,
            position=c.position,
            content=c.content,
            source_table=c.source_table,
            source_field=c.source_field,
            columns=c.columns,
            repeat_over=c.repeat_over,
            transformations=c.transformations,
            sort_order=c.sort_order,
        )
        for c in (tm.components or [])
    ]
    return Template(
        id=tm.id,
        name=tm.name,
        output_format=tm.output_format,
        excel_config=tm.excel_config,
        components=components,
    )


def _build_link_config(lm: LinkConfigModel) -> LinkConfig:
    tables = []
    for t in lm.tables:
        link = None
        if "link" in t and t["link"]:
            ld = t["link"]
            link = LinkDef(
                field=ld["field"],
                ref_table=ld["ref_table"],
                ref_field=ld["ref_field"],
            )
        tables.append(TableConfig(name=t["name"], primary_key=t["primary_key"], link=link))
    return LinkConfig(id=lm.id, name=lm.name, tables=tables)


@router.post("/generate")
async def generate(body: GenerateDocumentRequest) -> StreamingResponse:
    async with get_session() as session:
        tm = await session.get(TemplateModel, body.template_id)
        if not tm:
            raise HTTPException(status_code=404, detail="Template not found")
        ds = await session.get(DataSourceModel, body.data_source_id)
        if not ds:
            raise HTTPException(status_code=404, detail="Data source not found")
        lm = await session.get(LinkConfigModel, body.link_config_id)
        if not lm:
            raise HTTPException(status_code=404, detail="Link config not found")

    template = _build_template(tm)
    link_config = _build_link_config(lm)
    adapter = create_data_adapter(ds.db_type, ds.db_url)
    try:
        buf, content_type = await generate_document(
            template=template,
            adapter=adapter,
            link_config=link_config,
            selected_ids=body.selected_ids or None,
        )
    finally:
        await adapter.close()

    ext = "xlsx" if template.output_format == "xlsx" else "docx"
    filename = f"{template.name}.{ext}"
    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type=content_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
