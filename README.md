# E-commerce Sales Analytics Dashboard

An end-to-end data analytics project: a synthetic e-commerce orders dataset, a Pandas/NumPy
analysis pipeline, MySQL analytical queries, and an interactive Streamlit dashboard.

## Overview

- **Dataset:** 5,000 synthetic orders (Jan 2024 – May 2025) across 4 regions, 4 categories,
  20 products, 4 customer segments, and 5 payment methods. Generated reproducibly with a
  fixed random seed — no real customer data involved.
- **KPIs tracked:** total revenue, total orders, average order value (AOV), monthly revenue
  trend, month-over-month growth, top products, revenue by region/category, customer
  segment mix, and payment method mix.

## Project structure

```
ecommerce-sales-analytics/
├── generate_data.py      # Synthetic dataset generator -> data/ecommerce_orders.csv
├── analysis.py           # Pandas/NumPy KPI analysis, prints console summary
├── dashboard.py          # Interactive Streamlit dashboard
├── requirements.txt      # Python dependencies
├── data/
│   └── ecommerce_orders.csv
├── sql/
│   └── queries.sql       # MySQL 8.0 analytical queries (window functions, RANK, LAG)
└── README.md
```

## Dataset description

| Column           | Description                              |
|------------------|------------------------------------------|
| order_id         | Unique order identifier (ORD-000001 …)   |
| order_date       | Order date (YYYY-MM-DD)                  |
| region           | North / South / East / West              |
| category         | Electronics / Fashion / Home & Kitchen / Sports |
| product_name     | Product purchased                        |
| quantity         | Units ordered                            |
| unit_price       | Price per unit (USD)                     |
| revenue          | quantity × unit_price                    |
| customer_segment | New / Returning / Loyal / Corporate      |
| payment_method   | Credit Card / Debit Card / UPI / Net Banking / Wallet |

## How to run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate the dataset
python generate_data.py

# 3. Run the analysis (prints KPI summary to console)
python analysis.py

# 4. Launch the dashboard
streamlit run dashboard.py
```

## SQL highlights (`sql/queries.sql`)

MySQL 8.0-compatible analytical queries demonstrating:

1. **Monthly revenue with running total** — `SUM() OVER (ORDER BY ...)` window function
2. **Top 3 products per category** — `RANK() OVER (PARTITION BY category ...)`
3. **Regional performance comparison** — revenue, orders, AOV, and revenue share via a
   windowed grand total
4. **Customer segment AOV** — orders, revenue, AOV, and units per segment
5. **Month-over-month growth** — `LAG()` over monthly aggregates
6. **Category × Region matrix** — pivot-style conditional aggregation

Load the CSV into MySQL with `LOAD DATA INFILE` (see the commented example at the top
of `queries.sql`).

## Dashboard features

- KPI cards: total revenue, total orders, AOV, top region
- Monthly revenue trend line chart
- Bar charts: revenue by category and by region
- Customer segment breakdown table (orders, revenue, AOV)
- Sidebar filters: region, category, and date range — all visuals update live

## Tech stack

Python · Pandas · NumPy · Streamlit · MySQL (queries) · CSV
