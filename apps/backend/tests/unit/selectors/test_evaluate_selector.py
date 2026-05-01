from docuweave.use_cases.selectors.evaluate_selector import evaluate_selector
from docuweave.domain.entities.selector import SelectorConfig

JOBS = [
    {"job_id": "job_1", "job_name": "Engineer", "department": "Engineering"},
    {"job_id": "job_2", "job_name": "Designer", "department": "Design"},
    {"job_id": "job_3", "job_name": "Manager", "department": "Management"},
]

CONFIG = SelectorConfig(
    type="table_selector",
    table="jobs",
    display_fields=("job_id", "job_name", "department"),
    multi_select=True,
)


def test_single_select_filters_to_one() -> None:
    result = evaluate_selector(JOBS, CONFIG, selected_ids=["job_1"])
    assert len(result) == 1
    assert result[0]["job_id"] == "job_1"


def test_multi_select_filters_to_multiple() -> None:
    result = evaluate_selector(JOBS, CONFIG, selected_ids=["job_1", "job_3"])
    assert len(result) == 2
    ids = {r["job_id"] for r in result}
    assert ids == {"job_1", "job_3"}


def test_no_selection_returns_empty() -> None:
    result = evaluate_selector(JOBS, CONFIG, selected_ids=[])
    assert result == []


def test_unknown_id_returns_empty() -> None:
    result = evaluate_selector(JOBS, CONFIG, selected_ids=["nonexistent"])
    assert result == []


def test_preserves_all_row_fields() -> None:
    result = evaluate_selector(JOBS, CONFIG, selected_ids=["job_2"])
    assert result[0]["department"] == "Design"
