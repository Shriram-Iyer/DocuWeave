from dataclasses import dataclass, field
from typing import Any

from docuweave.domain.value_objects.field_type import FieldType


@dataclass(frozen=True)
class TransformationStep:
    op: str
    # For concat: list of field references (each may have nested transformations)
    fields: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    # For aggregation ops
    group_field: str = ""
    value_field: str = ""
    # For math ops
    operand: float | None = None
    # For array ops
    expression: str = ""


@dataclass(frozen=True)
class FieldTransformation:
    """A single output field with its type and transformation pipeline."""
    output_field: str
    field_type: FieldType
    pipeline: tuple[TransformationStep, ...] = field(default_factory=tuple)
