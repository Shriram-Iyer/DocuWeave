from docuweave.use_cases.data_fetch.join_tables import join_tables
from docuweave.domain.entities.table_link import LinkConfig, LinkDef, TableConfig


def make_link_config() -> LinkConfig:
    return LinkConfig(
        id="lc1",
        name="Test Links",
        tables=(
            TableConfig(name="jobs", primary_key="job_id"),
            TableConfig(
                name="users",
                primary_key="user_id",
                link=LinkDef(field="job_id", ref_table="jobs", ref_field="job_id"),
            ),
        ),
    )


JOBS = [
    {"job_id": "job_1", "job_name": "Engineer"},
    {"job_id": "job_2", "job_name": "Designer"},
]

USERS = [
    {"user_id": "u_1", "name": "Alice", "job_id": "job_1"},
    {"user_id": "u_2", "name": "Bob", "job_id": "job_1"},
    {"user_id": "u_3", "name": "Carol", "job_id": "job_2"},
]


def test_hash_map_join_one_to_many() -> None:
    tables_data = {"jobs": JOBS, "users": USERS}
    result = join_tables(tables_data, make_link_config())

    job_1 = next(j for j in result["jobs"] if j["job_id"] == "job_1")
    assert len(job_1["users"]) == 2
    user_names = {u["name"] for u in job_1["users"]}
    assert user_names == {"Alice", "Bob"}


def test_join_with_missing_parent_key_skips() -> None:
    orphan_users = [{"user_id": "u_99", "name": "Orphan", "job_id": "nonexistent"}]
    tables_data = {"jobs": JOBS, "users": orphan_users}
    result = join_tables(tables_data, make_link_config())
    for job in result["jobs"]:
        assert job.get("users", []) == []


def test_join_preserves_root_table_fields() -> None:
    tables_data = {"jobs": JOBS, "users": USERS}
    result = join_tables(tables_data, make_link_config())
    job_1 = next(j for j in result["jobs"] if j["job_id"] == "job_1")
    assert job_1["job_name"] == "Engineer"


def test_join_multiple_child_tables() -> None:
    targets = [
        {"target_id": "t_1", "job_id": "job_1", "amount": 5000},
        {"target_id": "t_2", "job_id": "job_2", "amount": 3000},
    ]
    config = LinkConfig(
        id="lc2",
        name="Multi",
        tables=(
            TableConfig(name="jobs", primary_key="job_id"),
            TableConfig(
                name="users",
                primary_key="user_id",
                link=LinkDef(field="job_id", ref_table="jobs", ref_field="job_id"),
            ),
            TableConfig(
                name="targets",
                primary_key="target_id",
                link=LinkDef(field="job_id", ref_table="jobs", ref_field="job_id"),
            ),
        ),
    )
    tables_data = {"jobs": JOBS, "users": USERS, "targets": targets}
    result = join_tables(tables_data, config)

    job_1 = next(j for j in result["jobs"] if j["job_id"] == "job_1")
    assert len(job_1["users"]) == 2
    assert len(job_1["targets"]) == 1
    assert job_1["targets"][0]["amount"] == 5000
