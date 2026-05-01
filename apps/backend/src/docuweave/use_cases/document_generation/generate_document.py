"""
Document generation orchestrator.
Pipeline: fetch tables → join → filter by selector → transform → render.
"""
import io
from typing import Any

from docuweave.adapters.db.base_adapter import BaseDataAdapter
from docuweave.domain.entities.selector import SelectorConfig
from docuweave.domain.entities.table_link import LinkConfig
from docuweave.domain.entities.template import Template
from docuweave.use_cases.data_fetch.fetch_tables_parallel import fetch_tables_parallel
from docuweave.use_cases.data_fetch.join_tables import join_tables
from docuweave.use_cases.selectors.evaluate_selector import evaluate_selector
from docuweave.use_cases.document_generation.render_word import render_word
from docuweave.use_cases.document_generation.render_excel import render_excel


async def generate_document(
    template: Template,
    adapter: BaseDataAdapter,
    link_config: LinkConfig,
    selector_config: SelectorConfig | None = None,
    selected_ids: list[str] | None = None,
) -> tuple[io.BytesIO, str]:
    """
    Orchestrate the full generation pipeline.

    Returns:
        (buffer, content_type) — the generated document as in-memory bytes + MIME type.
    """
    # 1. Determine which tables to fetch
    table_names = [t.name for t in link_config.tables]

    # 2. Fetch all tables in parallel — no SQL joins
    tables_data = await fetch_tables_parallel(adapter, table_names)

    # 3. Apply selector filter if provided
    if selector_config and selected_ids:
        filtered_rows = evaluate_selector(
            tables_data.get(selector_config.table, []),
            selector_config,
            selected_ids,
        )
        tables_data[selector_config.table] = filtered_rows

    # 4. Join tables in memory using link config
    joined_data = join_tables(tables_data, link_config)

    # 5. Render
    if template.output_format == "xlsx":
        buf = render_excel(template, data=joined_data)
        content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    else:
        buf = render_word(template, data=joined_data)
        content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    return buf, content_type
