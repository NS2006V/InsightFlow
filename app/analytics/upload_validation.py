"""
Pure validation logic for uploaded datasets.

Everything in this file works on a plain pandas DataFrame and returns
plain Python data (lists/dicts) -- no Flask, no file handling, no database.
That is what makes it possible to unit-test with a 2-row DataFrame built
by hand, with no web server or file upload involved.
"""

import pandas as pd

# The fixed V1 schema every uploaded dataset must match.
REQUIRED_COLUMNS = [
    "Order_ID",
    "Order_Date",
    "Customer_ID",
    "Product",
    "Category",
    "Region",
    "Quantity",
    "Unit_Price",
    "Discount",
    "Revenue",
]

# Columns that must hold dates / numbers respectively.
DATE_COLUMNS = ["Order_Date"]
NUMERIC_COLUMNS = ["Quantity", "Unit_Price", "Discount", "Revenue"]


def find_missing_columns(df):
    """Return the required columns that are absent from df, in schema order."""
    return [col for col in REQUIRED_COLUMNS if col not in df.columns]


def find_type_issues(df):
    """
    Check that date/numeric columns actually hold date-like/numeric values.

    Approach: convert a COPY of each column with errors="coerce" (values
    that can't be converted become NaN/NaT), then compare how many values
    were non-null BEFORE conversion vs. AFTER. If conversion produced
    extra missing values, that many original values were not valid for
    that column's expected type.

    Returns a dict such as:
        {"Quantity": 1, "Order_Date": 2}
    mapping column name -> number of values that failed conversion.
    Columns with no issues (or that don't exist yet) are left out.
    """
    issues = {}

    for col in DATE_COLUMNS:
        if col not in df.columns:
            continue  # a missing column is reported separately
        before = df[col].notna().sum()
        after = pd.to_datetime(df[col], errors="coerce").notna().sum()
        bad_count = before - after
        if bad_count > 0:
            issues[col] = int(bad_count)

    for col in NUMERIC_COLUMNS:
        if col not in df.columns:
            continue
        before = df[col].notna().sum()
        after = pd.to_numeric(df[col], errors="coerce").notna().sum()
        bad_count = before - after
        if bad_count > 0:
            issues[col] = int(bad_count)

    return issues


def validate_dataset(df):
    """
    Run every Phase 1 check on an already-loaded DataFrame.

    Returns:
        {
            "is_valid": bool,
            "missing_columns": [...],
            "type_issues": {...},
        }

    Type checks are skipped when required columns are missing -- a column
    that isn't there can't be meaningfully type-checked.
    """
    missing_columns = find_missing_columns(df)

    if missing_columns:
        return {
            "is_valid": False,
            "missing_columns": missing_columns,
            "type_issues": {},
        }

    type_issues = find_type_issues(df)

    return {
        "is_valid": len(type_issues) == 0,
        "missing_columns": [],
        "type_issues": type_issues,
    }
