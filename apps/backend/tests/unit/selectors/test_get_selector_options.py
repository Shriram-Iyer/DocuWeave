from docuweave.use_cases.selectors.get_selector_options import get_selector_options
from docuweave.domain.entities.selector import SelectorConfig

JOBS = [
    {"job_id": "job_1", "job_name": "Engineer", "department": "Engineering", "internal_code": "E001"},
    {"job_id": "job_2", "job_name": "Designer", "department": "Design", "internal_code": "D001"},
]

CONFIG = SelectorConfig(
    type="table_selector",
    table="jobs",
    display_fields=("job_id", "job_name", "department"),
    multi_select=True,
)


def test_returns_only_display_fields() -> None:
    options = get_selector_options(JOBS, CONFIG)
    for opt in options:
        assert "internal_code" not in opt
        assert set(opt.keys()) == {"job_id", "job_name", "department"}


def test_returns_all_rows() -> None:
    options = get_selector_options(JOBS, CONFIG)
    assert len(options) == 2


def test_empty_dataset_returns_empty() -> None:
    options = get_selector_options([], CONFIG)
    assert options == []
