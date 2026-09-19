import pandas as pd

from app.analytics.data_cleaning import clean_dataset


def make_valid_dataframe():
    return pd.DataFrame(
        {
            "Order_ID": ["ORD001", "ORD002", "ORD003"],
            "Order_Date": [
                "2026-01-05",
                "2026-01-08",
                "2026-01-12",
            ],
            "Customer_ID": ["CUST001", "CUST002", "CUST003"],
            "Product": ["Laptop", "Mouse", "Keyboard"],
            "Category": ["Electronics", "Accessories", "Accessories"],
            "Region": ["South", "South", "North"],
            "Quantity": [2, 3, 2],
            "Unit_Price": [50000, 1000, 2000],
            "Discount": [0.10, 0.05, 0.10],
            "Revenue": [1, 1, 1],
        }
    )


def test_recalculates_revenue():
    df = make_valid_dataframe()

    result = clean_dataset(df)
    cleaned = result["cleaned_df"]

    assert cleaned.loc[0, "Revenue"] == 90000.00
    assert cleaned.loc[1, "Revenue"] == 2850.00
    assert cleaned.loc[2, "Revenue"] == 3600.00


def test_converts_date_column():
    df = make_valid_dataframe()

    result = clean_dataset(df)
    cleaned = result["cleaned_df"]

    assert pd.api.types.is_datetime64_any_dtype(cleaned["Order_Date"])


def test_removes_duplicates():
    df = make_valid_dataframe()
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)

    result = clean_dataset(df)

    assert result["rows_before"] == 4
    assert result["rows_after"] == 3
    assert result["duplicates_removed"] == 1


def test_removes_invalid_rows():
    df = make_valid_dataframe()

    df.loc[1, "Quantity"] = -5
    df.loc[2, "Discount"] = 1.5

    result = clean_dataset(df)

    assert result["rows_after"] == 1
    assert result["invalid_rows_removed"] == 2


def test_preserves_valid_rows():
    df = make_valid_dataframe()

    result = clean_dataset(df)

    assert result["rows_before"] == 3
    assert result["rows_after"] == 3
    assert result["invalid_rows_removed"] == 0