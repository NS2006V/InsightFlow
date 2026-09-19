"""
Unit tests for app/analytics/upload_validation.py.

These use plain pandas DataFrames built by hand -- no file upload, no
Flask app -- because the analytics layer doesn't need either. This is
the fast, isolated layer of the test suite.
"""

import pandas as pd

from app.analytics.upload_validation import (
    REQUIRED_COLUMNS,
    find_missing_columns,
    find_type_issues,
    validate_dataset,
)


def _valid_dataframe():
    """A minimal 2-row DataFrame that satisfies the V1 schema."""
    return pd.DataFrame({
        "Order_ID": ["O1", "O2"],
        "Order_Date": ["2024-01-01", "2024-01-02"],
        "Customer_ID": ["C1", "C2"],
        "Product": ["Widget", "Gadget"],
        "Category": ["Tools", "Tools"],
        "Region": ["South", "North"],
        "Quantity": [2, 3],
        "Unit_Price": [100.0, 50.0],
        "Discount": [0, 10],
        "Revenue": [200.0, 135.0],
    })


def test_valid_dataset_has_no_issues():
    df = _valid_dataframe()
    result = validate_dataset(df)
    assert result["is_valid"] is True
    assert result["missing_columns"] == []
    assert result["type_issues"] == {}


def test_missing_required_column_is_detected():
    df = _valid_dataframe().drop(columns=["Region"])

    assert find_missing_columns(df) == ["Region"]

    result = validate_dataset(df)
    assert result["is_valid"] is False
    assert result["missing_columns"] == ["Region"]


def test_invalid_numeric_value_is_detected():
    df = _valid_dataframe()
    df.loc[0, "Quantity"] = "not-a-number"

    issues = find_type_issues(df)
    assert issues.get("Quantity") == 1

    result = validate_dataset(df)
    assert result["is_valid"] is False
    assert result["type_issues"]["Quantity"] == 1


def test_invalid_date_value_is_detected():
    df = _valid_dataframe()
    df.loc[1, "Order_Date"] = "not-a-date"

    issues = find_type_issues(df)
    assert issues.get("Order_Date") == 1

    result = validate_dataset(df)
    assert result["type_issues"]["Order_Date"] == 1


def test_required_columns_constant_matches_schema():
    # Guards against the fixed V1 schema drifting by accident.
    assert REQUIRED_COLUMNS == [
        "Order_ID", "Order_Date", "Customer_ID", "Product", "Category",
        "Region", "Quantity", "Unit_Price", "Discount", "Revenue",
    ]
