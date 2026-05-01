from docuweave.domain.value_objects.field_type import FieldType
from docuweave.domain.value_objects.operation import (
    accepts_field_type,
    is_aggregation,
)


def test_uppercase_accepts_string() -> None:
    assert accepts_field_type("uppercase", FieldType.STRING) is True


def test_uppercase_rejects_number() -> None:
    assert accepts_field_type("uppercase", FieldType.NUMBER) is False


def test_sum_by_group_accepts_number() -> None:
    assert accepts_field_type("sum_by_group", FieldType.NUMBER) is True


def test_sum_by_group_rejects_string() -> None:
    assert accepts_field_type("sum_by_group", FieldType.STRING) is False


def test_count_by_group_accepts_string_and_number() -> None:
    assert accepts_field_type("count_by_group", FieldType.STRING) is True
    assert accepts_field_type("count_by_group", FieldType.NUMBER) is True


def test_unknown_op_returns_false() -> None:
    assert accepts_field_type("nonexistent_op", FieldType.STRING) is False


def test_aggregation_ops_identified() -> None:
    assert is_aggregation("sum_by_group") is True
    assert is_aggregation("count_by_group") is True
    assert is_aggregation("avg_by_group") is True
    assert is_aggregation("min_by_group") is True
    assert is_aggregation("max_by_group") is True


def test_row_level_ops_not_aggregation() -> None:
    assert is_aggregation("uppercase") is False
    assert is_aggregation("concat") is False
    assert is_aggregation("add") is False
