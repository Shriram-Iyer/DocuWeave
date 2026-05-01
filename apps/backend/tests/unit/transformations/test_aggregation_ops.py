from docuweave.use_cases.transformations.aggregation_ops import (
    avg_by_group,
    count_by_group,
    max_by_group,
    min_by_group,
    sum_by_group,
)


SAMPLE = [
    {"job_id": "job_1", "salary": 5000},
    {"job_id": "job_1", "salary": 5000},
    {"job_id": "job_2", "salary": 3000},
]


def test_sum_by_group() -> None:
    result = sum_by_group(SAMPLE, "job_id", "salary")
    assert result["job_1"] == 10000
    assert result["job_2"] == 3000


def test_count_by_group() -> None:
    result = count_by_group(SAMPLE, "job_id")
    assert result["job_1"] == 2
    assert result["job_2"] == 1


def test_avg_by_group() -> None:
    result = avg_by_group(SAMPLE, "job_id", "salary")
    assert result["job_1"] == 5000.0
    assert result["job_2"] == 3000.0


def test_min_by_group() -> None:
    data = [
        {"job_id": "job_1", "salary": 4000},
        {"job_id": "job_1", "salary": 6000},
    ]
    result = min_by_group(data, "job_id", "salary")
    assert result["job_1"] == 4000


def test_max_by_group() -> None:
    data = [
        {"job_id": "job_1", "salary": 4000},
        {"job_id": "job_1", "salary": 6000},
    ]
    result = max_by_group(data, "job_id", "salary")
    assert result["job_1"] == 6000


def test_sum_by_group_empty_dataset() -> None:
    result = sum_by_group([], "job_id", "salary")
    assert result == {}


def test_sum_by_group_single_group() -> None:
    data = [{"dept": "eng", "count": 1}, {"dept": "eng", "count": 2}]
    result = sum_by_group(data, "dept", "count")
    assert result["eng"] == 3
