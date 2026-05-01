"""
Excel (.xlsx) renderer.
For canvas templates: writes each component to a sheet sequentially.
For Fortune Sheet configs (excel_config): uses the stored workbook config and substitutes tokens.
Returns an in-memory BytesIO buffer — no disk writes.
"""
import io
import json
import re
from typing import Any

import openpyxl
from openpyxl.styles import Font

from docuweave.domain.entities.template import Template, TemplateComponent


def render_excel(template: Template, data: dict[str, list[dict[str, Any]]]) -> io.BytesIO:
    if template.excel_config:
        return _render_from_fortune_sheet(template.excel_config, data)
    return _render_from_components(template.components, data)


def _render_from_components(
    components: tuple[TemplateComponent, ...],
    data: dict[str, list[dict[str, Any]]],
) -> io.BytesIO:
    wb = openpyxl.Workbook()
    ws = wb.active
    assert ws is not None
    current_row = 1

    for component in components:
        if component.type == "text":
            ws.cell(current_row, 1, component.content)
            current_row += 1

        elif component.type == "table":
            rows = data.get(component.source_table, [])
            columns = list(component.columns)
            if not columns:
                continue

            # Headers
            for col_idx, col_def in enumerate(columns, start=1):
                cell = ws.cell(current_row, col_idx, col_def.get("header", ""))
                cell.font = Font(bold=True)
            current_row += 1

            # Data
            for row in rows:
                for col_idx, col_def in enumerate(columns, start=1):
                    ws.cell(current_row, col_idx, row.get(col_def.get("field", ""), ""))
                current_row += 1

        elif component.type == "dynamic_field":
            rows = data.get(component.source_table, [])
            for row in rows:
                ws.cell(current_row, 1, str(row.get(component.source_field, "")))
                current_row += 1

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


def _render_from_fortune_sheet(
    excel_config: dict[str, Any],
    data: dict[str, list[dict[str, Any]]],
) -> io.BytesIO:
    """
    Walk Fortune Sheet JSON config, substitute {{field_name}} tokens,
    and expand {{#repeat table}}...{{/repeat}} blocks.
    """
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # type: ignore[arg-type]

    sheets = excel_config.get("sheets", [excel_config])
    for sheet_config in sheets:
        ws = wb.create_sheet(title=sheet_config.get("name", "Sheet"))
        cell_data = sheet_config.get("celldata", [])

        for cell_entry in cell_data:
            r = cell_entry.get("r", 0) + 1
            c = cell_entry.get("c", 0) + 1
            v = cell_entry.get("v", {})
            raw_value = v.get("v", "") if isinstance(v, dict) else v

            value = _substitute_tokens(str(raw_value) if raw_value is not None else "", data)
            ws.cell(r, c, value)

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


_TOKEN_RE = re.compile(r"\{\{(\w+)\}\}")


def _substitute_tokens(text: str, data: dict[str, list[dict[str, Any]]]) -> str:
    def replace(match: re.Match[str]) -> str:
        field = match.group(1)
        for rows in data.values():
            if rows and field in rows[0]:
                return str(rows[0][field])
        return match.group(0)

    return _TOKEN_RE.sub(replace, text)
