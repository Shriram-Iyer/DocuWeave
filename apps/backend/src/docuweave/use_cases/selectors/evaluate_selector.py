"""
Filter a dataset down to the rows matching selected IDs.
Pure function — no DB access.
"""
from typing import Any

from docuweave.domain.entities.selector import SelectorConfig


def evaluate_selector(
    rows: list[dict[str, Any]],
    config: SelectorConfig,
    selected_ids: list[str],
) -> list[dict[str, Any]]:
    """
    Return only rows whose primary display field value is in selected_ids.
    The primary key field is assumed to be the first display_field.
    """
    if not selected_ids:
        return []

    pk_field = config.display_fields[0] if config.display_fields else "id"
    selected_set = set(selected_ids)
    return [row for row in rows if str(row.get(pk_field, "")) in selected_set]
