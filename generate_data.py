"""
generate_data.py — Synthetic E-commerce Orders Dataset Generator

Generates a realistic ~5,000-row e-commerce orders dataset and saves it to
data/ecommerce_orders.csv. A fixed random seed is used for reproducibility.

Columns:
    order_id, order_date, region, category, product_name,
    quantity, unit_price, revenue, customer_segment, payment_method
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Fixed seed for reproducibility
RANDOM_SEED = 42

# Output configuration
OUTPUT_PATH = Path(__file__).resolve().parent / "data" / "ecommerce_orders.csv"
N_ROWS = 5000
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 5, 31)

REGIONS = ["North", "South", "East", "West"]

# Product catalog: category -> list of (product_name, base_price)
CATALOG = {
    "Electronics": [
        ("Wireless Headphones", 79.99),
        ("Smart Watch", 149.99),
        ("Bluetooth Speaker", 49.99),
        ("Laptop Stand", 39.99),
        ("USB-C Hub", 29.99),
    ],
    "Fashion": [
        ("Denim Jacket", 89.99),
        ("Running Shoes", 119.99),
        ("Cotton T-Shirt", 24.99),
        ("Leather Wallet", 45.99),
        ("Sunglasses", 59.99),
    ],
    "Home & Kitchen": [
        ("Air Fryer", 99.99),
        ("Ceramic Cookware Set", 129.99),
        ("Robot Vacuum", 249.99),
        ("LED Desk Lamp", 34.99),
        ("Memory Foam Pillow", 39.99),
    ],
    "Sports": [
        ("Yoga Mat", 29.99),
        ("Dumbbell Set", 89.99),
        ("Cycling Helmet", 54.99),
        ("Resistance Bands", 19.99),
        ("Camping Tent", 139.99),
    ],
}

CUSTOMER_SEGMENTS = ["New", "Returning", "Loyal", "Corporate"]
PAYMENT_METHODS = ["Credit Card", "Debit Card", "UPI", "Net Banking", "Wallet"]

# Segment purchase-probability weights (returning/loyal customers buy more often)
SEGMENT_WEIGHTS = [0.30, 0.35, 0.20, 0.15]


def random_date(start: datetime, end: datetime) -> datetime:
    """Return a random date between start and end (inclusive)."""
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def main() -> None:
    random.seed(RANDOM_SEED)

    products = [
        (category, name, price)
        for category, items in CATALOG.items()
        for name, price in items
    ]

    rows = []
    for i in range(1, N_ROWS + 1):
        order_date = random_date(START_DATE, END_DATE)
        region = random.choice(REGIONS)
        category, product_name, base_price = random.choice(products)

        # Quantity: mostly 1-2, occasionally bulk
        quantity = random.choices([1, 2, 3, 4, 5], weights=[55, 25, 10, 6, 4])[0]

        # Small price jitter (+/-5%) to mimic discounts / price changes
        unit_price = round(base_price * random.uniform(0.95, 1.05), 2)
        revenue = round(quantity * unit_price, 2)

        segment = random.choices(CUSTOMER_SEGMENTS, weights=SEGMENT_WEIGHTS)[0]
        payment_method = random.choice(PAYMENT_METHODS)

        rows.append(
            {
                "order_id": f"ORD-{i:06d}",
                "order_date": order_date.strftime("%Y-%m-%d"),
                "region": region,
                "category": category,
                "product_name": product_name,
                "quantity": quantity,
                "unit_price": unit_price,
                "revenue": revenue,
                "customer_segment": segment,
                "payment_method": payment_method,
            }
        )

    fieldnames = [
        "order_id",
        "order_date",
        "region",
        "category",
        "product_name",
        "quantity",
        "unit_price",
        "revenue",
        "customer_segment",
        "payment_method",
    ]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows):,} rows -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
