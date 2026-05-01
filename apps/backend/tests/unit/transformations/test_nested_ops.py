from docuweave.use_cases.transformations.execute_pipeline import execute_pipeline


def run(row: dict, pipeline: list[dict]) -> object:
    return execute_pipeline(row, pipeline, dataset=[row])


def test_concat_with_inner_uppercase() -> None:
    row = {"first_name": "john", "last_name": "doe"}
    pipeline = [
        {
            "op": "concat",
            "fields": [
                {"field": "first_name", "transformations": [{"op": "uppercase", "source_field": "first_name"}]},
                {"literal": " "},
                {"field": "last_name"},
            ],
        }
    ]
    assert run(row, pipeline) == "JOHN doe"


def test_concat_with_inner_lowercase_and_uppercase() -> None:
    row = {"a": "HELLO", "b": "world"}
    pipeline = [
        {
            "op": "concat",
            "fields": [
                {"field": "a", "transformations": [{"op": "lowercase", "source_field": "a"}]},
                {"literal": "-"},
                {"field": "b", "transformations": [{"op": "uppercase", "source_field": "b"}]},
            ],
        }
    ]
    assert run(row, pipeline) == "hello-WORLD"


def test_concat_three_fields_no_inner_transforms() -> None:
    row = {"x": "A", "y": "B", "z": "C"}
    pipeline = [
        {
            "op": "concat",
            "fields": [
                {"field": "x"},
                {"field": "y"},
                {"field": "z"},
            ],
        }
    ]
    assert run(row, pipeline) == "ABC"
