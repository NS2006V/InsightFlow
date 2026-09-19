import pandas as pd

from app.analytics.data_cleaning import clean_dataset
from app.analytics.sales_analytics import (
    calculate_sales_metrics,
    revenue_by_month,
    revenue_by_category,
    revenue_by_region,
    top_products,
)


def prepare_dashboard_data(df: pd.DataFrame) -> dict:
    """
    Clean uploaded data and prepare all core analytics
    required by the InsightFlow dashboard.
    """

    cleaning_result = clean_dataset(df)
    cleaned_df = cleaning_result["cleaned_df"]

    metrics = calculate_sales_metrics(cleaned_df)

    return {
        "cleaning": {
            "rows_before": cleaning_result["rows_before"],
            "rows_after": cleaning_result["rows_after"],
            "duplicates_removed": cleaning_result["duplicates_removed"],
            "invalid_rows_removed": cleaning_result["invalid_rows_removed"],
        },
        "metrics": metrics,
        "monthly_revenue": revenue_by_month(cleaned_df),
        "category_revenue": revenue_by_category(cleaned_df),
        "region_revenue": revenue_by_region(cleaned_df),
        "top_products": top_products(cleaned_df),
    }