import pytest
from docuweave.use_cases.transformations.execute_pipeline import execute_pipeline
from docuweave.domain.value_objects.field_type import FieldType


def run(row: dict, pipeline: list[dict]) -> object:
    return execute_pipeline(row, pipeline, dataset=[row])


def test_uppercase() -> None:
    result = run({"name": "hello"}, [{"op": "uppercase", "source_field": "name"}])
    assert result == "HELLO"


def test_lowercase() -> None:
    result = run({"name": "HELLO"}, [{"op": "lowercase", "source_field": "name"}])
    assert result == "hello"


def test_concat_two_fields() -> None:
    row = {"first": "John", "last": "Doe"}
    pipeline = [
        {
            "op": "concat",
            "fields": [
                {"field": "first"},
                {"literal": " "},
                {"field": "last"},
            ],
        }
    ]
    assert run(row, pipeline) == "John Doe"


def test_add() -> None:
    result = run({"val": 5}, [{"op": "add", "source_field": "val", "operand": 3}])
    assert result == 8


def test_subtract() -> None:
    result = run({"val": 10}, [{"op": "subtract", "source_field": "val", "operand": 4}])
    assert result == 6


def test_multiply() -> None:
    result = run({"val": 5}, [{"op": "multiply", "source_field": "val", "operand": 3}])
    assert result == 15


def test_divide() -> None:
    result = run({"val": 9}, [{"op": "divide", "source_field": "val", "operand": 3}])
    assert result == 3.0


def test_divide_by_zero_raises() -> None:
    with pytest.raises(ZeroDivisionError):
        run({"val": 9}, [{"op": "divide", "source_field": "val", "operand": 0}])
