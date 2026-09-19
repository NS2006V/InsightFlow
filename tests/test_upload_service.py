"""
Tests for app/services/upload_service.py -- the layer that reads an
uploaded file and runs it through validation.

We simulate a browser upload with Werkzeug's FileStorage wrapped around
an in-memory BytesIO buffer, so these tests need no real files on disk
and no running Flask server.
"""

import io

from werkzeug.datastructures import FileStorage

from app.services.upload_service import process_upload

VALID_CSV = (
    "Order_ID,Order_Date,Customer_ID,Product,Category,Region,"
    "Quantity,Unit_Price,Discount,Revenue\n"
    "O1,2024-01-01,C1,Widget,Tools,South,2,100,0,200\n"
    "O2,2024-01-02,C2,Gadget,Tools,North,3,50,10,135\n"
)

MISSING_COLUMN_CSV = (
    "Order_ID,Order_Date,Customer_ID,Product,Category,"  # Region left out
    "Quantity,Unit_Price,Discount,Revenue\n"
    "O1,2024-01-01,C1,Widget,Tools,2,100,0,200\n"
)

BAD_TYPES_CSV = (
    "Order_ID,Order_Date,Customer_ID,Product,Category,Region,"
    "Quantity,Unit_Price,Discount,Revenue\n"
    "O1,2024-01-01,C1,Widget,Tools,South,not-a-number,100,0,200\n"
)


def _file(content, filename):
    return FileStorage(stream=io.BytesIO(content.encode("utf-8")), filename=filename)


def test_valid_csv_passes():
    result = process_upload(_file(VALID_CSV, "sales.csv"))
    assert result["success"] is True
    assert result["errors"] == []
    assert result["summary"]["row_count"] == 2


def test_missing_column_is_rejected():
    result = process_upload(_file(MISSING_COLUMN_CSV, "sales.csv"))
    assert result["success"] is False
    assert any("Region" in err for err in result["errors"])


def test_unsupported_extension_is_rejected():
    result = process_upload(_file(VALID_CSV, "sales.txt"))
    assert result["success"] is False
    assert any("Unsupported file type" in err for err in result["errors"])


def test_invalid_numeric_value_is_rejected():
    result = process_upload(_file(BAD_TYPES_CSV, "sales.csv"))
    assert result["success"] is False
    assert any("Quantity" in err for err in result["errors"])


def test_no_file_selected():
    result = process_upload(None)
    assert result["success"] is False
    assert "No file was selected." in result["errors"]
