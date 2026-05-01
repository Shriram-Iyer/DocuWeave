from typing import Any
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select, delete

from docuweave.infrastructure.database.sql.engine import get_session
from docuweave.infrastructure.database.sql.models import TemplateModel, ComponentModel
from docuweave.adapters.http.schemas.template_schemas import (
    TemplateCreateRequest,
    TemplateUpdateRequest,
    TemplateResponse,
    ComponentCreateRequest,
    ComponentResponse,
    CanvasPositionSchema,
)

router = APIRouter(prefix="/api/v1/templates", tags=["templates"])


def _model_to_response(t: TemplateModel) -> TemplateResponse:
    return TemplateResponse(
        id=t.id,
        name=t.name,
        output_format=t.output_format,
        excel_config=t.excel_config,
        components=[
            ComponentResponse(
                id=c.id,
                template_id=c.template_id,
                type=c.type,
                position=CanvasPositionSchema(**c.position) if isinstance(c.position, dict) else CanvasPositionSchema(),
                content=c.content,
                source_table=c.source_table,
                source_field=c.source_field,
                columns=c.columns,
                repeat_over=c.repeat_over,
                transformations=c.transformations,
                sort_order=c.sort_order,
            )
            for c in (t.components or [])
        ],
    )


@router.get("", response_model=list[TemplateResponse])
async def list_templates() -> list[TemplateResponse]:
    async with get_session() as session:
        result = await session.execute(select(TemplateModel))
        return [_model_to_response(t) for t in result.scalars().all()]


@router.post("", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(body: TemplateCreateRequest) -> TemplateResponse:
    async with get_session() as session:
        template = TemplateModel(
            id=str(uuid.uuid4()),
            name=body.name,
            output_format=body.output_format,
            excel_config=body.excel_config,
        )
        session.add(template)
        await session.commit()
        await session.refresh(template)
        return _model_to_response(template)


@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(template_id: str) -> TemplateResponse:
    async with get_session() as session:
        t = await session.get(TemplateModel, template_id)
        if not t:
            raise HTTPException(status_code=404, detail="Template not found")
        return _model_to_response(t)


@router.put("/{template_id}", response_model=TemplateResponse)
async def update_template(template_id: str, body: TemplateUpdateRequest) -> TemplateResponse:
    async with get_session() as session:
        t = await session.get(TemplateModel, template_id)
        if not t:
            raise HTTPException(status_code=404, detail="Template not found")
        if body.name is not None:
            t.name = body.name
        if body.output_format is not None:
            t.output_format = body.output_format
        if body.excel_config is not None:
            t.excel_config = body.excel_config
        t.updated_at = datetime.now(timezone.utc)
        await session.commit()
        await session.refresh(t)
        return _model_to_response(t)


@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(template_id: str) -> None:
    async with get_session() as session:
        t = await session.get(TemplateModel, template_id)
        if not t:
            raise HTTPException(status_code=404, detail="Template not found")
        await session.delete(t)
        await session.commit()


@router.get("/{template_id}/components", response_model=list[ComponentResponse])
async def list_components(template_id: str) -> list[ComponentResponse]:
    async with get_session() as session:
        t = await session.get(TemplateModel, template_id)
        if not t:
            raise HTTPException(status_code=404, detail="Template not found")
        return [
            ComponentResponse(
                id=c.id,
                template_id=c.template_id,
                type=c.type,
                position=CanvasPositionSchema(**c.position) if isinstance(c.position, dict) else CanvasPositionSchema(),
                content=c.content,
                source_table=c.source_table,
                source_field=c.source_field,
                columns=c.columns,
                repeat_over=c.repeat_over,
                transformations=c.transformations,
                sort_order=c.sort_order,
            )
            for c in (t.components or [])
        ]


@router.post(
    "/{template_id}/components",
    response_model=ComponentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_component(template_id: str, body: ComponentCreateRequest) -> ComponentResponse:
    async with get_session() as session:
        t = await session.get(TemplateModel, template_id)
        if not t:
            raise HTTPException(status_code=404, detail="Template not found")
        component = ComponentModel(
            id=str(uuid.uuid4()),
            template_id=template_id,
            type=body.type,
            position=body.position.model_dump(),
            content=body.content,
            source_table=body.source_table,
            source_field=body.source_field,
            columns=body.columns,
            repeat_over=body.repeat_over,
            transformations=body.transformations,
            sort_order=body.sort_order,
        )
        session.add(component)
        await session.commit()
        await session.refresh(component)
        return ComponentResponse(
            id=component.id,
            template_id=component.template_id,
            type=component.type,
            position=body.position,
            content=component.content,
            source_table=component.source_table,
            source_field=component.source_field,
            columns=component.columns,
            repeat_over=component.repeat_over,
            transformations=component.transformations,
            sort_order=component.sort_order,
        )


@router.put("/{template_id}/components/{component_id}", response_model=ComponentResponse)
async def update_component(
    template_id: str, component_id: str, body: ComponentCreateRequest
) -> ComponentResponse:
    async with get_session() as session:
        c = await session.get(ComponentModel, component_id)
        if not c or c.template_id != template_id:
            raise HTTPException(status_code=404, detail="Component not found")
        c.type = body.type
        c.position = body.position.model_dump()
        c.content = body.content
        c.source_table = body.source_table
        c.source_field = body.source_field
        c.columns = body.columns
        c.repeat_over = body.repeat_over
        c.transformations = body.transformations
        c.sort_order = body.sort_order
        await session.commit()
        await session.refresh(c)
        return ComponentResponse(
            id=c.id,
            template_id=c.template_id,
            type=c.type,
            position=body.position,
            content=c.content,
            source_table=c.source_table,
            source_field=c.source_field,
            columns=c.columns,
            repeat_over=c.repeat_over,
            transformations=c.transformations,
            sort_order=c.sort_order,
        )


@router.delete(
    "/{template_id}/components/{component_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_component(template_id: str, component_id: str) -> None:
    async with get_session() as session:
        c = await session.get(ComponentModel, component_id)
        if not c or c.template_id != template_id:
            raise HTTPException(status_code=404, detail="Component not found")
        await session.delete(c)
        await session.commit()
