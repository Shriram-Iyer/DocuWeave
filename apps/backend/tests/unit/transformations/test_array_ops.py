import pytest
from docuweave.use_cases.transformations.execute_pipeline import execute_pipeline


def test_map_uppercase_each():
    row = {"tags": ["hello", "world"]}
    pipeline = [
        {
            "op": "map",
            "source_field": "tags",
            "transformations": [{"op": "uppercase", "source_field": "item"}],
        }
    ]
    result = execute_pipeline(row, pipeline, dataset=[row])
    assert result == ["HELLO", "WORLD"]


def test_filter_by_field_value():
    row = {
        "items": [
            {"type": "a", "value": 1},
            {"type": "b", "value": 2},
            {"type": "a", "value": 3},
        ]
    }
    pipeline = [{"op": "filter", "source_field": "items", "field": "type", "value": "a"}]
    result = execute_pipeline(row, pipeline, dataset=[row])
    assert result == [{"type": "a", "value": 1}, {"type": "a", "value": 3}]


def test_reduce_sum():
    row = {"numbers": [1, 2, 3, 4]}
    pipeline = [{"op": "reduce", "source_field": "numbers", "agg": "sum"}]
    result = execute_pipeline(row, pipeline, dataset=[row])
    assert result == 10.0


def test_reduce_count():
    row = {"items": ["a", "b", "c"]}
    pipeline = [{"op": "reduce", "source_field": "items", "agg": "count"}]
    result = execute_pipeline(row, pipeline, dataset=[row])
    assert result == 3


def test_reduce_min():
    row = {"scores": [5, 3, 8, 1]}
    pipeline = [{"op": "reduce", "source_field": "scores", "agg": "min"}]
    result = execute_pipeline(row, pipeline, dataset=[row])
    assert result == 1


def test_reduce_max():
    row = {"scores": [5, 3, 8, 1]}
    pipeline = [{"op": "reduce", "source_field": "scores", "agg": "max"}]
    result = execute_pipeline(row, pipeline, dataset=[row])
    assert result == 8


def test_reduce_unknown_agg_raises():
    row = {"items": [1, 2]}
    pipeline = [{"op": "reduce", "source_field": "items", "agg": "product"}]
    with pytest.raises(ValueError, match="Unknown reduce agg"):
        execute_pipeline(row, pipeline, dataset=[row])


def test_filter_empty_result():
    row = {"items": [{"type": "x"}]}
    pipeline = [{"op": "filter", "source_field": "items", "field": "type", "value": "z"}]
    result = execute_pipeline(row, pipeline, dataset=[row])
    assert result == []
