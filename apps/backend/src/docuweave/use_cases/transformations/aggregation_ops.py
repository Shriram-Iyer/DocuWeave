"""
Pure aggregation functions — operate on full dataset, not a single row.
Each returns a dict keyed by group value → aggregated result.
"""
from typing import Any


def sum_by_group(dataset: list[dict[str, Any]], group_field: str, value_field: str) -> dict[str, float]:
    result: dict[str, float] = {}
    for row in dataset:
        key = str(row[group_field])
        result[key] = result.get(key, 0.0) + float(row[value_field])
    return result


def count_by_group(dataset: list[dict[str, Any]], group_field: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for row in dataset:
        key = str(row[group_field])
        result[key] = result.get(key, 0) + 1
    return result


def avg_by_group(dataset: list[dict[str, Any]], group_field: str, value_field: str) -> dict[str, float]:
    totals: dict[str, float] = {}
    counts: dict[str, int] = {}
    for row in dataset:
        key = str(row[group_field])
        totals[key] = totals.get(key, 0.0) + float(row[value_field])
        counts[key] = counts.get(key, 0) + 1
    return {k: totals[k] / counts[k] for k in totals}


def min_by_group(dataset: list[dict[str, Any]], group_field: str, value_field: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for row in dataset:
        key = str(row[group_field])
        val = row[value_field]
        if key not in result or val < result[key]:
            result[key] = val
    return result


def max_by_group(dataset: list[dict[str, Any]], group_field: str, value_field: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for row in dataset:
        key = str(row[group_field])
        val = row[value_field]
        if key not in result or val > result[key]:
            result[key] = val
    return result
