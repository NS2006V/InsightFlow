import pandas as pd


def calculate_sales_metrics(df: pd.DataFrame) -> dict:
    """Calculate the main sales KPIs."""

    total_revenue = round(df["Revenue"].sum(), 2)
    total_orders = df["Order_ID"].nunique()
    total_quantity = int(df["Quantity"].sum())

    average_order_value = (
        round(total_revenue / total_orders, 2)
        if total_orders > 0
        else 0.0
    )

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "total_quantity": total_quantity,
        "average_order_value": average_order_value,
    }


def revenue_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate total revenue for each month."""

    result = (
        df.assign(
            Month=df["Order_Date"].dt.to_period("M").astype(str)
        )
        .groupby("Month", as_index=False)["Revenue"]
        .sum()
        .sort_values("Month")
        .reset_index(drop=True)
    )

    result["Revenue"] = result["Revenue"].round(2)

    return result


def revenue_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate revenue by product category."""

    result = (
        df.groupby("Category", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
        .reset_index(drop=True)
    )

    result["Revenue"] = result["Revenue"].round(2)

    return result


def revenue_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate revenue by region."""

    result = (
        df.groupby("Region", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
        .reset_index(drop=True)
    )

    result["Revenue"] = result["Revenue"].round(2)

    return result


def top_products(df: pd.DataFrame, limit: int = 5) -> pd.DataFrame:
    """Return the top products by revenue."""

    result = (
        df.groupby("Product", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
        .head(limit)
        .reset_index(drop=True)
    )

    result["Revenue"] = result["Revenue"].round(2)

    return result