from fastapi.testclient import TestClient


def test_validate_valid_pipeline(client: TestClient) -> None:
    response = client.post(
        "/api/v1/transformations/validate",
        json={
            "field_type": "string",
            "pipeline": [{"op": "uppercase", "source_field": "name"}],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["is_valid"] is True
    assert body["errors"] == []


def test_validate_invalid_op_on_wrong_type(client: TestClient) -> None:
    response = client.post(
        "/api/v1/transformations/validate",
        json={
            "field_type": "string",
            "pipeline": [{"op": "sum_by_group", "group_field": "id", "value_field": "salary"}],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["is_valid"] is False
    assert len(body["errors"]) > 0


def test_validate_unknown_field_type(client: TestClient) -> None:
    response = client.post(
        "/api/v1/transformations/validate",
        json={"field_type": "supertype", "pipeline": []},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["is_valid"] is False


def test_preview_returns_transformed_value(client: TestClient) -> None:
    response = client.post(
        "/api/v1/transformations/preview",
        json={
            "field_type": "string",
            "pipeline": [{"op": "uppercase", "source_field": "name"}],
            "sample_data": {"name": "hello"},
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["result"] == "HELLO"
    assert body["errors"] == []


def test_preview_returns_error_for_invalid_pipeline(client: TestClient) -> None:
    response = client.post(
        "/api/v1/transformations/preview",
        json={
            "field_type": "string",
            "pipeline": [{"op": "add", "source_field": "val", "operand": 1}],
            "sample_data": {"val": "not_a_number"},
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["result"] is None
    assert len(body["errors"]) > 0
