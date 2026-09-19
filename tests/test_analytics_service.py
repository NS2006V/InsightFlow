import pandas as pd

from app.services.analytics_service import prepare_dashboard_data


def make_test_dataframe():
    return pd.DataFrame(
        {
            "Order_ID": [
                "ORD001",
                "ORD002",
                "ORD003",
            ],
            "Order_Date": [
                "2026-01-05",
                "2026-01-08",
                "2026-02-02",
            ],
            "Customer_ID": [
                "CUST001",
                "CUST002",
                "CUST003",
            ],
            "Product": [
                "Laptop",
                "Mouse",
                "Monitor",
            ],
            "Category": [
                "Electronics",
                "Accessories",
                "Electronics",
            ],
            "Region": [
                "South",
                "South",
                "West",
            ],
            "Quantity": [2, 3, 1],
            "Unit_Price": [50000, 1000, 15000],
            "Discount": [0.10, 0.05, 0.05],
            "Revenue": [1, 1, 1],
        }
    )


def test_prepare_dashboard_data():
    df = make_test_dataframe()

    result = prepare_dashboard_data(df)

    assert "cleaning" in result
    assert "metrics" in result
    assert "monthly_revenue" in result
    assert "category_revenue" in result
    assert "region_revenue" in result
    assert "top_products" in result


def test_dashboard_metrics_are_correct():
    df = make_test_dataframe()

    result = prepare_dashboard_data(df)

    metrics = result["metrics"]

    assert metrics["total_revenue"] == 107100.00
    assert metrics["total_orders"] == 3
    assert metrics["total_quantity"] == 6
    assert metrics["average_order_value"] == 35700.00


def test_dashboard_cleaning_information():
    df = make_test_dataframe()

    result = prepare_dashboard_data(df)

    cleaning = result["cleaning"]

    assert cleaning["rows_before"] == 3
    assert cleaning["rows_after"] == 3
    assert cleaning["duplicates_removed"] == 0
    assert cleaning["invalid_rows_removed"] == 0