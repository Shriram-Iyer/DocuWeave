import pytest
from docuweave.domain.value_objects.field_type import FieldType


def test_all_field_types_have_string_values() -> None:
    assert FieldType.STRING == "string"
    assert FieldType.NUMBER == "number"
    assert FieldType.BOOLEAN == "boolean"
    assert FieldType.DATE == "date"
    assert FieldType.ARRAY == "array"
    assert FieldType.OBJECT == "object"


def test_field_type_from_string() -> None:
    assert FieldType("string") == FieldType.STRING
    assert FieldType("number") == FieldType.NUMBER


def test_invalid_field_type_raises() -> None:
    with pytest.raises(ValueError):
        FieldType("invalid")
