import pandas as pd

from app.analytics.sales_analytics import (
    calculate_sales_metrics,
    revenue_by_month,
    revenue_by_category,
    revenue_by_region,
    top_products,
)


def make_clean_dataframe():
    return pd.DataFrame(
        {
            "Order_ID": [
                "ORD001",
                "ORD002",
                "ORD003",
                "ORD004",
                "ORD005",
            ],
            "Order_Date": pd.to_datetime(
                [
                    "2026-01-05",
                    "2026-01-08",
                    "2026-01-12",
                    "2026-02-02",
                    "2026-02-10",
                ]
            ),
            "Customer_ID": [
                "CUST001",
                "CUST002",
                "CUST003",
                "CUST001",
                "CUST004",
            ],
            "Product": [
                "Laptop",
                "Mouse",
                "Keyboard",
                "Monitor",
                "Laptop",
            ],
            "Category": [
                "Electronics",
                "Accessories",
                "Accessories",
                "Electronics",
                "Electronics",
            ],
            "Region": [
                "South",
                "South",
                "North",
                "West",
                "East",
            ],
            "Quantity": [2, 3, 2, 1, 1],
            "Unit_Price": [50000, 1000, 2000, 15000, 50000],
            "Discount": [0.10, 0.05, 0.10, 0.05, 0.00],
            "Revenue": [90000, 2850, 3600, 14250, 50000],
        }
    )


def test_calculate_sales_metrics():
    df = make_clean_dataframe()

    result = calculate_sales_metrics(df)

    assert result["total_revenue"] == 160700.00
    assert result["total_orders"] == 5
    assert result["total_quantity"] == 9
    assert result["average_order_value"] == 32140.00


def test_revenue_by_month():
    df = make_clean_dataframe()

    result = revenue_by_month(df)

    assert list(result["Month"]) == ["2026-01", "2026-02"]
    assert list(result["Revenue"]) == [96450.00, 64250.00]


def test_revenue_by_category():
    df = make_clean_dataframe()

    result = revenue_by_category(df)

    assert list(result["Category"]) == [
        "Electronics",
        "Accessories",
    ]

    assert list(result["Revenue"]) == [
        154250.00,
        6450.00,
    ]


def test_revenue_by_region():
    df = make_clean_dataframe()

    result = revenue_by_region(df)

    assert list(result["Region"]) == [
        "South",
        "East",
        "West",
        "North",
    ]

    assert list(result["Revenue"]) == [
        92850.00,
        50000.00,
        14250.00,
        3600.00,
    ]


def test_top_products():
    df = make_clean_dataframe()

    result = top_products(df, limit=2)

    assert list(result["Product"]) == [
        "Laptop",
        "Monitor",
    ]

    assert list(result["Revenue"]) == [
        140000.00,
        14250.00,
    ]