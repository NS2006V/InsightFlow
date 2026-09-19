"""
Upload service: turns an uploaded file into a validated DataFrame plus a
plain-English report the route can hand straight to a template.

This is the only layer that touches file I/O (reading the upload into
pandas). Routes call this; app/analytics/upload_validation.py never sees
a raw uploaded file or Flask's `request` object -- that separation is
what lets the validation logic be unit-tested with plain DataFrames and
no web server running at all.
"""

import pandas as pd

from app.utils.file_validators import has_allowed_extension
from app.analytics.upload_validation import validate_dataset, REQUIRED_COLUMNS


def read_dataset(file_storage):
    """
    Read an uploaded CSV or XLSX file into a pandas DataFrame.

    Args:
        file_storage: a Werkzeug FileStorage (what Flask gives you from
                      request.files[...]), or any file-like object with
                      a `.filename` attribute.

    Returns:
        pandas.DataFrame

    Raises:
        ValueError: if the file cannot be parsed as CSV/Excel.
    """
    filename = file_storage.filename.lower()

    try:
        if filename.endswith(".csv"):
            return pd.read_csv(file_storage)
        return pd.read_excel(file_storage)
    except Exception as exc:
        # Wrap pandas/openpyxl's raw error in one clear message -- the
        # user doesn't need to see a library traceback.
        raise ValueError(f"Could not read file as a valid CSV/Excel file: {exc}")


def process_upload(file_storage):
    """
    Full Phase 1 pipeline: check the file, parse it, validate its schema
    and data types.

    Returns a dict, always safe to render in a template:
        {
            "success": bool,
            "errors": ["...", ...],          # empty list if all checks passed
            "summary": {"row_count": int, "columns": [...]} or None,
        }
    """
    if file_storage is None or file_storage.filename == "":
        return {"success": False, "errors": ["No file was selected."], "summary": None}

    if not has_allowed_extension(file_storage.filename):
        return {
            "success": False,
            "errors": [
                "Unsupported file type. Please upload a .csv or .xlsx file. "
                f"Required columns: {', '.join(REQUIRED_COLUMNS)}."
            ],
            "summary": None,
        }

    try:
        df = read_dataset(file_storage)
    except ValueError as exc:
        return {"success": False, "errors": [str(exc)], "summary": None}

    result = validate_dataset(df)
    errors = []

    if result["missing_columns"]:
        errors.append(
            "Missing required column(s): " + ", ".join(result["missing_columns"])
        )

    for column, bad_count in result["type_issues"].items():
        kind = "dates" if column == "Order_Date" else "numbers"
        errors.append(f"Column '{column}' has {bad_count} value(s) that are not valid {kind}.")

    summary = None
    if not result["missing_columns"]:
        summary = {"row_count": len(df), "columns": list(df.columns)}

    return {
        "success": result["is_valid"],
        "errors": errors,
        "summary": summary,
    }
