-- ============================================================================
-- queries.sql — E-commerce Sales Analytics (MySQL 8.0+)
--
-- Assumes a table named `ecommerce_orders` with columns:
--   order_id, order_date (DATE), region, category, product_name,
--   quantity, unit_price, revenue, customer_segment, payment_method
--
-- Load the CSV (example):
--   LOAD DATA INFILE '/path/to/ecommerce_orders.csv'
--   INTO TABLE ecommerce_orders
--   FIELDS TERMINATED BY ',' ENCLOSED BY '"'
--   LINES TERMINATED BY '\n' IGNORE 1 ROWS;
-- ============================================================================

-- 1. Monthly revenue with running total (window function) ---------------------
SELECT
    DATE_FORMAT(order_date, '%Y-%m')            AS order_month,
    COUNT(*)                                   AS total_orders,
    ROUND(SUM(revenue), 2)                     AS monthly_revenue,
    ROUND(SUM(SUM(revenue)) OVER (
        ORDER BY DATE_FORMAT(order_date, '%Y-%m')
    ), 2)                                      AS running_total
FROM ecommerce_orders
GROUP BY order_month
ORDER BY order_month;


-- 2. Top 3 products per category by revenue, using RANK() --------------------
SELECT category, product_name, product_revenue, revenue_rank
FROM (
    SELECT
        category,
        product_name,
        ROUND(SUM(revenue), 2) AS product_revenue,
        RANK() OVER (
            PARTITION BY category
            ORDER BY SUM(revenue) DESC
        ) AS revenue_rank
    FROM ecommerce_orders
    GROUP BY category, product_name
) ranked
WHERE revenue_rank <= 3
ORDER BY category, revenue_rank;


-- 3. Regional performance comparison (revenue, orders, AOV, share) -----------
SELECT
    region,
    COUNT(*)                        AS total_orders,
    ROUND(SUM(revenue), 2)           AS total_revenue,
    ROUND(AVG(revenue), 2)           AS avg_order_value,
    ROUND(
        SUM(revenue) / SUM(SUM(revenue)) OVER () * 100, 2
    )                               AS revenue_share_pct
FROM ecommerce_orders
GROUP BY region
ORDER BY total_revenue DESC;


-- 4. Customer segment AOV and order mix --------------------------------------
SELECT
    customer_segment,
    COUNT(*)               AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(revenue), 2) AS avg_order_value,
    ROUND(SUM(quantity), 0) AS units_sold
FROM ecommerce_orders
GROUP BY customer_segment
ORDER BY total_revenue DESC;


-- 5. Month-over-month growth using LAG() -------------------------------------
SELECT
    order_month,
    monthly_revenue,
    prev_month_revenue,
    ROUND(
        (monthly_revenue - prev_month_revenue) / prev_month_revenue * 100, 2
    ) AS mom_growth_pct
FROM (
    SELECT
        DATE_FORMAT(order_date, '%Y-%m') AS order_month,
        ROUND(SUM(revenue), 2)          AS monthly_revenue,
        LAG(ROUND(SUM(revenue), 2)) OVER (
            ORDER BY DATE_FORMAT(order_date, '%Y-%m')
        )                               AS prev_month_revenue
    FROM ecommerce_orders
    GROUP BY order_month
) m
ORDER BY order_month;


-- 6. Category x Region matrix (pivot-style revenue) ---------------------------
SELECT
    category,
    ROUND(SUM(CASE WHEN region = 'North' THEN revenue ELSE 0 END), 2) AS north,
    ROUND(SUM(CASE WHEN region = 'South' THEN revenue ELSE 0 END), 2) AS south,
    ROUND(SUM(CASE WHEN region = 'East'  THEN revenue ELSE 0 END), 2) AS east,
    ROUND(SUM(CASE WHEN region = 'West'  THEN revenue ELSE 0 END), 2) AS west,
    ROUND(SUM(revenue), 2) AS total
FROM ecommerce_orders
GROUP BY category
ORDER BY total DESC;
