"""
dashboard.py — E-commerce Sales Analytics Dashboard (Streamlit)

Interactive dashboard over data/ecommerce_orders.csv:
    - KPI cards: total revenue, total orders, AOV, top region
    - Revenue trend line chart
    - Category / region bar charts
    - Sidebar filters: region, category, date range

Run:
    streamlit run dashboard.py
"""

from pathlib import Path

import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).resolve().parent / "data" / "ecommerce_orders.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load and cache the orders dataset."""
    df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    return df


def kpi_card(label: str, value: str) -> None:
    """Render a simple KPI card using Streamlit metric styling."""
    st.metric(label=label, value=value)


def main() -> None:
    st.set_page_config(
        page_title="E-commerce Sales Analytics",
        page_icon="🛒",
        layout="wide",
    )

    st.title("🛒 E-commerce Sales Analytics Dashboard")
    st.caption("Interactive sales performance overview · synthetic dataset")

    df = load_data()
    if df.empty:
        st.warning("No data found. Run `python generate_data.py` first.")
        return

    # ---------------- Sidebar filters ----------------
    st.sidebar.header("Filters")

    regions = sorted(df["region"].unique())
    categories = sorted(df["category"].unique())

    selected_regions = st.sidebar.multiselect(
        "Region", options=regions, default=regions
    )
    selected_categories = st.sidebar.multiselect(
        "Category", options=categories, default=categories
    )

    min_date = df["order_date"].min().date()
    max_date = df["order_date"].max().date()
    date_range = st.sidebar.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # Apply filters
    filtered = df[
        df["region"].isin(selected_regions)
        & df["category"].isin(selected_categories)
    ]
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start, end = date_range
        filtered = filtered[
            (filtered["order_date"].dt.date >= start)
            & (filtered["order_date"].dt.date <= end)
        ]

    if filtered.empty:
        st.warning("No orders match the selected filters.")
        return

    # ---------------- KPI cards ----------------
    total_revenue = filtered["revenue"].sum()
    total_orders = len(filtered)
    aov = filtered["revenue"].mean()
    top_region = (
        filtered.groupby("region")["revenue"].sum().idxmax()
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        kpi_card("Total Revenue", f"${total_revenue:,.2f}")
    with col2:
        kpi_card("Total Orders", f"{total_orders:,}")
    with col3:
        kpi_card("Avg Order Value", f"${aov:,.2f}")
    with col4:
        kpi_card("Top Region", top_region)

    st.divider()

    # ---------------- Revenue trend ----------------
    st.subheader("Monthly Revenue Trend")
    monthly = (
        filtered.assign(order_month=filtered["order_date"].dt.to_period("M").astype(str))
        .groupby("order_month")["revenue"]
        .sum()
        .reset_index()
        .sort_values("order_month")
    )
    st.line_chart(monthly.set_index("order_month")["revenue"])

    # ---------------- Category / region bars ----------------
    left, right = st.columns(2)

    with left:
        st.subheader("Revenue by Category")
        by_category = (
            filtered.groupby("category")["revenue"]
            .sum()
            .sort_values(ascending=False)
        )
        st.bar_chart(by_category)

    with right:
        st.subheader("Revenue by Region")
        by_region = (
            filtered.groupby("region")["revenue"]
            .sum()
            .sort_values(ascending=False)
        )
        st.bar_chart(by_region)

    # ---------------- Segment breakdown ----------------
    st.subheader("Customer Segment Breakdown")
    by_segment = (
        filtered.groupby("customer_segment")
        .agg(orders=("order_id", "count"), revenue=("revenue", "sum"))
        .reset_index()
        .sort_values("revenue", ascending=False)
    )
    by_segment["aov"] = by_segment["revenue"] / by_segment["orders"]
    st.dataframe(by_segment, use_container_width=True, hide_index=True)

    # ---------------- Raw data ----------------
    with st.expander("View filtered data"):
        st.dataframe(filtered, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
