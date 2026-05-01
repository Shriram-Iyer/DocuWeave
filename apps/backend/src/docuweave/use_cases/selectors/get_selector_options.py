"""
Build the popup display rows — only the fields the developer declared as display_fields.
Pure function — no DB access.
"""
from typing import Any

from docuweave.domain.entities.selector import SelectorConfig


def get_selector_options(
    rows: list[dict[str, Any]],
    config: SelectorConfig,
) -> list[dict[str, Any]]:
    """Return each row projected to only the display_fields columns."""
    display = set(config.display_fields)
    return [{k: v for k, v in row.items() if k in display} for row in rows]
