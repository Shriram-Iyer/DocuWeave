"""
Server-side in-memory join using hash maps.
No SQL joins. Combines independently fetched tables using LinkConfig definitions.
"""
import copy
from typing import Any

from docuweave.domain.entities.table_link import LinkConfig


def join_tables(
    tables_data: dict[str, list[dict[str, Any]]],
    link_config: LinkConfig,
) -> dict[str, list[dict[str, Any]]]:
    """
    Attach child rows to their parent rows using the link config.

    For each child table that has a link:
    1. Build a hash map: parent_pk_value → list[child_row]
    2. For each parent row, attach the list as parent_row[child_table_name]

    Returns a new dict with the same structure as tables_data but with child
    rows attached to their parents. Root table rows are returned with children.
    """
    # Deep copy so we don't mutate the original dicts
    result: dict[str, list[dict[str, Any]]] = {
        name: [copy.copy(row) for row in rows]
        for name, rows in tables_data.items()
    }

    # Build index: table_name → {pk_value → row} for quick parent lookup
    pk_index: dict[str, dict[str, dict[str, Any]]] = {}
    for table_cfg in link_config.tables:
        pk = table_cfg.primary_key
        rows = result.get(table_cfg.name, [])
        pk_index[table_cfg.name] = {str(row[pk]): row for row in rows if pk in row}

    # Attach children to parents
    for table_cfg in link_config.tables:
        if table_cfg.link is None:
            continue  # root table — nothing to attach

        link = table_cfg.link
        child_rows = result.get(table_cfg.name, [])
        parent_index = pk_index.get(link.ref_table, {})

        # Build: parent_pk_value → [child_rows]
        children_map: dict[str, list[dict[str, Any]]] = {}
        for child_row in child_rows:
            parent_key = str(child_row.get(link.field, ""))
            children_map.setdefault(parent_key, []).append(child_row)

        # Attach to each parent row
        for parent_row in result.get(link.ref_table, []):
            parent_pk_val = str(parent_row.get(link.ref_field, ""))
            parent_row[table_cfg.name] = children_map.get(parent_pk_val, [])

    return result


def resolve_links(
    tables_data: dict[str, list[dict[str, Any]]],
    link_config: LinkConfig,
) -> dict[str, list[dict[str, Any]]]:
    """Alias for join_tables — same operation, named for clarity in callers."""
    return join_tables(tables_data, link_config)
