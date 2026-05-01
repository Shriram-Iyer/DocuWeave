"""
validate_pipeline(field_type, pipeline) -> (is_valid: bool, errors: list[str])

Validates:
1. Each op exists and accepts the given field_type
2. No more than one aggregation op in a pipeline
3. Inner (nested) transformations in concat.fields are validated separately
"""
from typing import Any

from docuweave.domain.value_objects.field_type import FieldType
from docuweave.domain.value_objects.operation import OPERATION_ACCEPTED_TYPES, is_aggregation


def validate_pipeline(
    field_type: FieldType, pipeline: list[dict[str, Any]]
) -> tuple[bool, list[str]]:
    errors: list[str] = []

    agg_count = sum(1 for step in pipeline if is_aggregation(step.get("op", "")))
    if agg_count > 1:
        errors.append(
            f"Multiple aggregation ops in one pipeline are not allowed (found {agg_count})."
        )

    for step in pipeline:
        op = step.get("op", "")

        if op not in OPERATION_ACCEPTED_TYPES:
            errors.append(f"Unknown operation: '{op}'.")
            continue

        accepted = OPERATION_ACCEPTED_TYPES[op]
        if field_type not in accepted:
            errors.append(
                f"Operation '{op}' does not accept field type '{field_type}' "
                f"(accepted: {sorted(t.value for t in accepted)})."
            )

        # Validate nested transformations inside concat fields
        if op == "concat":
            for field_spec in step.get("fields", []):
                inner_transforms = field_spec.get("transformations", [])
                if not inner_transforms:
                    continue
                inner_type_str = field_spec.get("field_type", FieldType.STRING)
                try:
                    inner_type = FieldType(inner_type_str)
                except ValueError:
                    errors.append(f"Unknown field_type in nested transform: '{inner_type_str}'.")
                    continue
                inner_valid, inner_errors = validate_pipeline(inner_type, inner_transforms)
                if not inner_valid:
                    errors.extend(f"(nested) {e}" for e in inner_errors)

    return len(errors) == 0, errors
