"""
analysis.py — E-commerce Sales Data Analysis

Loads data/ecommerce_orders.csv and computes core business KPIs:
    - Total revenue / total orders / average order value (AOV)
    - Monthly revenue trend + month-over-month growth
    - Top 10 products by revenue
    - Revenue by region and by category
    - Customer segment breakdown (orders, revenue, AOV)
    - Payment method mix

Run:
    python analysis.py
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

DATA_PATH = Path(__file__).resolve().parent / "data" / "ecommerce_orders.csv"


def load_data(path: Path) -> pd.DataFrame:
    """Load the orders CSV and parse dates."""
    df = pd.read_csv(path, parse_dates=["order_date"])
    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
    return df


def kpi_summary(df: pd.DataFrame) -> dict:
    """Compute headline KPIs."""
    return {
        "total_revenue": df["revenue"].sum(),
        "total_orders": len(df),
        "avg_order_value": df["revenue"].mean(),
        "total_units": int(df["quantity"].sum()),
        "avg_unit_price": df["unit_price"].mean(),
        "top_region": df.groupby("region")["revenue"].sum().idxmax(),
        "top_category": df.groupby("category")["revenue"].sum().idxmax(),
    }


def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Monthly revenue, orders, and month-over-month growth."""
    monthly = (
        df.groupby("order_month")
        .agg(revenue=("revenue", "sum"), orders=("order_id", "count"))
        .reset_index()
        .sort_values("order_month")
    )
    monthly["mom_growth_pct"] = monthly["revenue"].pct_change() * 100
    monthly["running_total"] = monthly["revenue"].cumsum()
    return monthly


def top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Top-N products by revenue."""
    return (
        df.groupby(["category", "product_name"])
        .agg(revenue=("revenue", "sum"), orders=("order_id", "count"),
             units=("quantity", "sum"))
        .reset_index()
        .sort_values("revenue", ascending=False)
        .head(n)
    )


def revenue_by_dimension(df: pd.DataFrame, dim: str) -> pd.DataFrame:
    """Revenue, orders and share by a categorical dimension."""
    grouped = (
        df.groupby(dim)
        .agg(revenue=("revenue", "sum"), orders=("order_id", "count"))
        .reset_index()
        .sort_values("revenue", ascending=False)
    )
    grouped["share_pct"] = grouped["revenue"] / grouped["revenue"].sum() * 100
    return grouped


def segment_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Orders, revenue and AOV per customer segment."""
    seg = (
        df.groupby("customer_segment")
        .agg(orders=("order_id", "count"), revenue=("revenue", "sum"))
        .reset_index()
        .sort_values("revenue", ascending=False)
    )
    seg["aov"] = seg["revenue"] / seg["orders"]
    seg["share_pct"] = seg["revenue"] / seg["revenue"].sum() * 100
    return seg


def print_report(df: pd.DataFrame) -> None:
    """Print a clean KPI summary to the console."""
    kpis = kpi_summary(df)
    monthly = monthly_trend(df)
    top10 = top_products(df)
    by_region = revenue_by_dimension(df, "region")
    by_category = revenue_by_dimension(df, "category")
    by_segment = segment_breakdown(df)
    by_payment = revenue_by_dimension(df, "payment_method")

    line = "=" * 60
    print(f"\n{line}")
    print("  E-COMMERCE SALES ANALYTICS — KPI SUMMARY")
    print(f"{line}")
    print(f"  Total Revenue        : ${kpis['total_revenue']:>12,.2f}")
    print(f"  Total Orders         : {kpis['total_orders']:>12,}")
    print(f"  Avg Order Value      : ${kpis['avg_order_value']:>12,.2f}")
    print(f"  Units Sold           : {kpis['total_units']:>12,}")
    print(f"  Top Region           : {kpis['top_region']:>12}")
    print(f"  Top Category         : {kpis['top_category']:>12}")
    print(f"{line}")

    print("\n-- Monthly Revenue Trend (MoM growth) --")
    print(monthly.to_string(index=False, float_format="%.2f"))

    print("\n-- Top 10 Products by Revenue --")
    print(top10.to_string(index=False, float_format="%.2f"))

    print("\n-- Revenue by Region --")
    print(by_region.to_string(index=False, float_format="%.2f"))

    print("\n-- Revenue by Category --")
    print(by_category.to_string(index=False, float_format="%.2f"))

    print("\n-- Customer Segment Breakdown --")
    print(by_segment.to_string(index=False, float_format="%.2f"))

    print("\n-- Payment Method Mix --")
    print(by_payment.to_string(index=False, float_format="%.2f"))
    print()


def main() -> int:
    if not DATA_PATH.exists():
        print(f"Dataset not found at {DATA_PATH}. Run generate_data.py first.")
        return 1
    df = load_data(DATA_PATH)
    print_report(df)
    return 0


if __name__ == "__main__":
    sys.exit(main())
