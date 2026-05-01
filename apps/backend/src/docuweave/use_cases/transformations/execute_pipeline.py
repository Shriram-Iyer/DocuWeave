"""
Pure transformation executor.

execute_pipeline(row, pipeline, dataset) -> Any

- row: the current data row being transformed
- pipeline: list of transformation step dicts
- dataset: full table rows (required for aggregation ops)

Aggregation ops are "dataset-level": they pre-compute over the entire dataset
and then look up the current row's group key. All other ops are "row-level".
"""
from typing import Any

from docuweave.use_cases.transformations.aggregation_ops import (
    avg_by_group,
    count_by_group,
    max_by_group,
    min_by_group,
    sum_by_group,
)


def _resolve_field(row: dict[str, Any], field_spec: dict[str, Any], dataset: list[dict[str, Any]]) -> Any:
    """Resolve a field reference within a concat op, applying any inner transformations."""
    if "literal" in field_spec:
        return str(field_spec["literal"])

    field_name = field_spec["field"]
    value = row.get(field_name, "")

    inner_transforms = field_spec.get("transformations", [])
    if inner_transforms:
        # Recursively apply inner pipeline starting from the field value
        inner_row = {field_name: value}
        value = execute_pipeline(inner_row, inner_transforms, dataset)

    return value


def execute_pipeline(row: dict[str, Any], pipeline: list[dict[str, Any]], dataset: list[dict[str, Any]]) -> Any:
    """
    Apply each transformation step sequentially.
    Returns the final transformed value.
    If the pipeline is empty, returns None.
    """
    current: Any = None

    for step in pipeline:
        op = step["op"]

        if op == "uppercase":
            source = step.get("source_field", "")
            val = row.get(source, current) if source else current
            current = str(val).upper()

        elif op == "lowercase":
            source = step.get("source_field", "")
            val = row.get(source, current) if source else current
            current = str(val).lower()

        elif op == "concat":
            parts = [str(_resolve_field(row, f, dataset)) for f in step.get("fields", [])]
            current = "".join(parts)

        elif op == "add":
            source = step.get("source_field", "")
            val = float(row.get(source, current) if source else current)
            current = val + float(step["operand"])

        elif op == "subtract":
            source = step.get("source_field", "")
            val = float(row.get(source, current) if source else current)
            current = val - float(step["operand"])

        elif op == "multiply":
            source = step.get("source_field", "")
            val = float(row.get(source, current) if source else current)
            current = val * float(step["operand"])

        elif op == "divide":
            source = step.get("source_field", "")
            val = float(row.get(source, current) if source else current)
            divisor = float(step["operand"])
            if divisor == 0:
                raise ZeroDivisionError("Division by zero in transformation pipeline")
            current = val / divisor

        # --- Aggregation ops (dataset-level) ---
        elif op == "sum_by_group":
            group_field = step["group_field"]
            value_field = step["value_field"]
            agg = sum_by_group(dataset, group_field, value_field)
            key = str(row.get(group_field, ""))
            current = agg.get(key, 0.0)

        elif op == "count_by_group":
            group_field = step["group_field"]
            agg = count_by_group(dataset, group_field)
            key = str(row.get(group_field, ""))
            current = agg.get(key, 0)

        elif op == "avg_by_group":
            group_field = step["group_field"]
            value_field = step["value_field"]
            agg = avg_by_group(dataset, group_field, value_field)
            key = str(row.get(group_field, ""))
            current = agg.get(key, 0.0)

        elif op == "min_by_group":
            group_field = step["group_field"]
            value_field = step["value_field"]
            agg = min_by_group(dataset, group_field, value_field)
            key = str(row.get(group_field, ""))
            current = agg.get(key)

        elif op == "max_by_group":
            group_field = step["group_field"]
            value_field = step["value_field"]
            agg = max_by_group(dataset, group_field, value_field)
            key = str(row.get(group_field, ""))
            current = agg.get(key)

        # --- Array ops (row-level) ---
        elif op == "map":
            source = step.get("source_field", "")
            arr = list(row.get(source, current) if source else (current or []))
            inner = step.get("transformations", [])
            current = [execute_pipeline({"item": item}, inner, dataset) for item in arr]

        elif op == "filter":
            source = step.get("source_field", "")
            arr = list(row.get(source, current) if source else (current or []))
            field = step.get("field", "")
            expected = step.get("value")
            current = [item for item in arr if (item.get(field) if isinstance(item, dict) else item) == expected]

        elif op == "reduce":
            source = step.get("source_field", "")
            arr = list(row.get(source, current) if source else (current or []))
            agg_op = step.get("agg", "sum")
            if agg_op == "sum":
                current = sum(float(item) for item in arr)
            elif agg_op == "count":
                current = len(arr)
            elif agg_op == "min":
                current = min(arr) if arr else None
            elif agg_op == "max":
                current = max(arr) if arr else None
            else:
                raise ValueError(f"Unknown reduce agg: {agg_op!r}")

        else:
            raise ValueError(f"Unknown transformation op: '{op}'")

    return current
