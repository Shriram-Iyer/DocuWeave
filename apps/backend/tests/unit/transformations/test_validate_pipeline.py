from docuweave.domain.value_objects.field_type import FieldType
from docuweave.use_cases.transformations.validate_pipeline import validate_pipeline


def test_valid_uppercase_on_string() -> None:
    is_valid, errors = validate_pipeline(
        FieldType.STRING,
        [{"op": "uppercase", "source_field": "name"}],
    )
    assert is_valid is True
    assert errors == []


def test_string_field_rejects_sum_by_group() -> None:
    is_valid, errors = validate_pipeline(
        FieldType.STRING,
        [{"op": "sum_by_group", "group_field": "id", "value_field": "salary"}],
    )
    assert is_valid is False
    assert any("sum_by_group" in e for e in errors)


def test_number_field_accepts_sum_by_group() -> None:
    is_valid, errors = validate_pipeline(
        FieldType.NUMBER,
        [{"op": "sum_by_group", "group_field": "id", "value_field": "salary"}],
    )
    assert is_valid is True
    assert errors == []


def test_multiple_aggregations_fails() -> None:
    is_valid, errors = validate_pipeline(
        FieldType.NUMBER,
        [
            {"op": "sum_by_group", "group_field": "id", "value_field": "salary"},
            {"op": "avg_by_group", "group_field": "id", "value_field": "salary"},
        ],
    )
    assert is_valid is False
    assert any("multiple aggregation" in e.lower() for e in errors)


def test_unknown_op_fails() -> None:
    is_valid, errors = validate_pipeline(
        FieldType.STRING,
        [{"op": "fly_to_moon"}],
    )
    assert is_valid is False
    assert any("unknown" in e.lower() or "fly_to_moon" in e for e in errors)


def test_empty_pipeline_is_valid() -> None:
    is_valid, errors = validate_pipeline(FieldType.STRING, [])
    assert is_valid is True
    assert errors == []


def test_nested_inner_transformation_validated() -> None:
    # Inner transformation uses uppercase on a number field — should fail
    is_valid, errors = validate_pipeline(
        FieldType.NUMBER,
        [
            {
                "op": "concat",
                "fields": [
                    {
                        "field": "name",
                        "transformations": [{"op": "sum_by_group", "group_field": "id", "value_field": "x"}],
                        "field_type": "string",  # inner field is string
                    }
                ],
            }
        ],
    )
    assert is_valid is False


def test_add_on_number_is_valid() -> None:
    is_valid, errors = validate_pipeline(
        FieldType.NUMBER,
        [{"op": "add", "source_field": "val", "operand": 1}],
    )
    assert is_valid is True
    assert errors == []


def test_add_on_string_is_invalid() -> None:
    is_valid, errors = validate_pipeline(
        FieldType.STRING,
        [{"op": "add", "source_field": "val", "operand": 1}],
    )
    assert is_valid is False
