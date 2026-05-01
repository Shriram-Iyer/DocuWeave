from enum import StrEnum

from docuweave.domain.value_objects.field_type import FieldType

# Maps each operation to the set of FieldTypes it accepts as input.
# Operations not listed here are invalid.
OPERATION_ACCEPTED_TYPES: dict[str, set[FieldType]] = {
    # Basic — string
    "uppercase": {FieldType.STRING},
    "lowercase": {FieldType.STRING},
    "concat": {FieldType.STRING},
    # Basic — numeric
    "add": {FieldType.NUMBER},
    "subtract": {FieldType.NUMBER},
    "multiply": {FieldType.NUMBER},
    "divide": {FieldType.NUMBER},
    # Aggregation — numeric only
    "sum_by_group": {FieldType.NUMBER},
    "count_by_group": {FieldType.NUMBER, FieldType.STRING, FieldType.DATE, FieldType.BOOLEAN},
    "avg_by_group": {FieldType.NUMBER},
    "min_by_group": {FieldType.NUMBER, FieldType.DATE},
    "max_by_group": {FieldType.NUMBER, FieldType.DATE},
    # Array operations
    "map": {FieldType.ARRAY},
    "filter": {FieldType.ARRAY},
    "reduce": {FieldType.ARRAY},
}

AGGREGATION_OPS: frozenset[str] = frozenset(
    {"sum_by_group", "count_by_group", "avg_by_group", "min_by_group", "max_by_group"}
)

ROW_LEVEL_OPS: frozenset[str] = frozenset(
    {"uppercase", "lowercase", "concat", "add", "subtract", "multiply", "divide", "map", "filter", "reduce"}
)


class Operation(StrEnum):
    UPPERCASE = "uppercase"
    LOWERCASE = "lowercase"
    CONCAT = "concat"
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    SUM_BY_GROUP = "sum_by_group"
    COUNT_BY_GROUP = "count_by_group"
    AVG_BY_GROUP = "avg_by_group"
    MIN_BY_GROUP = "min_by_group"
    MAX_BY_GROUP = "max_by_group"
    MAP = "map"
    FILTER = "filter"
    REDUCE = "reduce"


def accepts_field_type(op: str, field_type: FieldType) -> bool:
    accepted = OPERATION_ACCEPTED_TYPES.get(op)
    if accepted is None:
        return False
    return field_type in accepted


def is_aggregation(op: str) -> bool:
    return op in AGGREGATION_OPS
