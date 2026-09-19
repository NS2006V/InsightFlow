import pandas as pd


EXPECTED_COLUMNS = [
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


NUMERIC_COLUMNS = [
    "Quantity",
    "Unit_Price",
    "Discount",
    "Revenue",
]


def clean_dataset(df: pd.DataFrame) -> dict:
    """
    Clean and prepare a validated InsightFlow dataset.

    Returns:
        dict containing:
        - cleaned_df
        - rows_before
        - rows_after
        - duplicates_removed
        - missing_values_filled
        - invalid_rows_removed
    """

    cleaned = df.copy()

    rows_before = len(cleaned)

    # 1. Standardize column order
    cleaned = cleaned[EXPECTED_COLUMNS]

    # 2. Remove completely empty rows
    cleaned = cleaned.dropna(how="all")

    # 3. Remove duplicate records
    before_duplicates = len(cleaned)
    cleaned = cleaned.drop_duplicates()
    duplicates_removed = before_duplicates - len(cleaned)

    # 4. Convert date column
    cleaned["Order_Date"] = pd.to_datetime(
        cleaned["Order_Date"],
        errors="coerce",
    )

    # 5. Convert numeric columns
    for column in NUMERIC_COLUMNS:
        cleaned[column] = pd.to_numeric(
            cleaned[column],
            errors="coerce",
        )

    # 6. Remove rows with invalid essential values
    essential_columns = [
        "Order_ID",
        "Order_Date",
        "Customer_ID",
        "Product",
        "Category",
        "Region",
        "Quantity",
        "Unit_Price",
        "Discount",
    ]

    invalid_before = len(cleaned)

    cleaned = cleaned.dropna(subset=essential_columns)

    # Quantity and price cannot be negative
    cleaned = cleaned[
        (cleaned["Quantity"] > 0)
        & (cleaned["Unit_Price"] >= 0)
    ]

    # Discount should be between 0 and 1
    cleaned = cleaned[
        (cleaned["Discount"] >= 0)
        & (cleaned["Discount"] <= 1)
    ]

    invalid_rows_removed = invalid_before - len(cleaned)

    # 7. Recalculate revenue from transaction values
    cleaned["Revenue"] = (
        cleaned["Quantity"]
        * cleaned["Unit_Price"]
        * (1 - cleaned["Discount"])
    )

    cleaned["Revenue"] = cleaned["Revenue"].round(2)

    cleaned = cleaned.reset_index(drop=True)

    return {
        "cleaned_df": cleaned,
        "rows_before": rows_before,
        "rows_after": len(cleaned),
        "duplicates_removed": duplicates_removed,
        "missing_values_filled": 0,
        "invalid_rows_removed": invalid_rows_removed,
    }