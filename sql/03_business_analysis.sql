USE customer_shopping_analysis;


-- ============================================================
-- CUSTOMER SHOPPING BEHAVIOR ANALYSIS
-- BUSINESS ANALYSIS QUERIES
-- ============================================================


-- ============================================================
-- 1. REVENUE BY GENDER
-- ============================================================

SELECT
    gender,
    COUNT(*) AS total_purchases,
    SUM(purchase_amount_usd) AS total_revenue,
    ROUND(AVG(purchase_amount_usd), 2) AS average_purchase_amount
FROM customer_shopping
GROUP BY gender
ORDER BY total_revenue DESC;


-- ============================================================
-- 2. HIGH-SPENDING CUSTOMERS USING DISCOUNTS
-- ============================================================

SELECT
    customer_id,
    purchase_amount_usd,
    discount_applied,
    item_purchased,
    category
FROM customer_shopping
WHERE discount_applied = 'Yes'
  AND purchase_amount_usd > 75
ORDER BY purchase_amount_usd DESC;


-- ============================================================
-- 3. TOP 5 PRODUCTS BY AVERAGE RATING
-- ============================================================

SELECT
    item_purchased,
    ROUND(AVG(review_rating), 2) AS average_rating,
    COUNT(*) AS total_purchases
FROM customer_shopping
GROUP BY item_purchased
ORDER BY average_rating DESC
LIMIT 5;


-- ============================================================
-- 4. SHIPPING TYPE COMPARISON
-- ============================================================

SELECT
    shipping_type,
    COUNT(*) AS total_orders,
    ROUND(AVG(purchase_amount_usd), 2) AS average_purchase_amount,
    SUM(purchase_amount_usd) AS total_revenue
FROM customer_shopping
GROUP BY shipping_type
ORDER BY total_revenue DESC;


-- ============================================================
-- 5. SUBSCRIBERS VS NON-SUBSCRIBERS
-- ============================================================

SELECT
    subscription_status,
    COUNT(*) AS total_customers,
    ROUND(AVG(purchase_amount_usd), 2) AS average_purchase_amount,
    SUM(purchase_amount_usd) AS total_revenue,
    ROUND(AVG(previous_purchases), 2) AS average_previous_purchases
FROM customer_shopping
GROUP BY subscription_status
ORDER BY total_revenue DESC;


-- ============================================================
-- 6. DISCOUNT-DEPENDENT PRODUCTS
-- ============================================================

SELECT
    item_purchased,
    COUNT(*) AS total_purchases,
    SUM(discount_applied = 'Yes') AS discounted_purchases,
    ROUND(
        100.0 * SUM(discount_applied = 'Yes') / COUNT(*),
        2
    ) AS discount_usage_percentage
FROM customer_shopping
GROUP BY item_purchased
HAVING COUNT(*) >= 50
ORDER BY discount_usage_percentage DESC;


-- ============================================================
-- 7. CUSTOMER SEGMENTATION
-- ============================================================

SELECT
    customer_id,
    previous_purchases,
    CASE
        WHEN previous_purchases = 1 THEN 'New'
        WHEN previous_purchases BETWEEN 2 AND 10 THEN 'Returning'
        ELSE 'Loyal'
    END AS customer_segment
FROM customer_shopping
ORDER BY previous_purchases;


-- ============================================================
-- 8. TOP 3 PRODUCTS PER CATEGORY
-- ============================================================

WITH product_sales AS (
    SELECT
        category,
        item_purchased,
        COUNT(*) AS total_purchases,
        SUM(purchase_amount_usd) AS total_revenue,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY SUM(purchase_amount_usd) DESC
        ) AS product_rank
    FROM customer_shopping
    GROUP BY category, item_purchased
)

SELECT
    category,
    item_purchased,
    total_purchases,
    total_revenue,
    product_rank
FROM product_sales
WHERE product_rank <= 3
ORDER BY category, product_rank;


-- ============================================================
-- 9. REPEAT BUYERS AND SUBSCRIPTIONS
-- ============================================================

SELECT
    subscription_status,
    COUNT(*) AS repeat_buyers
FROM customer_shopping
WHERE previous_purchases > 1
GROUP BY subscription_status
ORDER BY repeat_buyers DESC;


-- ============================================================
-- 10. REVENUE BY AGE GROUP
-- ============================================================

SELECT
    age_group,
    COUNT(*) AS total_purchases,
    SUM(purchase_amount_usd) AS total_revenue,
    ROUND(AVG(purchase_amount_usd), 2) AS average_purchase_amount
FROM customer_shopping
GROUP BY age_group
ORDER BY total_revenue DESC;


-- =========================================================
-- QUERY 11: Overall Business KPIs
-- =========================================================

SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    SUM(purchase_amount_usd) AS total_revenue,
    ROUND(AVG(purchase_amount_usd), 2) AS average_order_value,
    ROUND(AVG(review_rating), 2) AS average_rating,
    ROUND(AVG(previous_purchases), 2) AS average_previous_purchases
FROM customer_shopping;


-- =========================================================
-- QUERY 12: Revenue by Category
-- =========================================================

SELECT
    category,
    COUNT(*) AS total_orders,
    SUM(purchase_amount_usd) AS total_revenue,
    ROUND(AVG(purchase_amount_usd), 2) AS average_order_value,
    ROUND(AVG(review_rating), 2) AS average_rating
FROM customer_shopping
GROUP BY category
ORDER BY total_revenue DESC;


-- =========================================================
-- QUERY 13: Discount vs Non-Discount Performance
-- =========================================================

SELECT
    discount_applied,
    COUNT(*) AS total_orders,
    SUM(purchase_amount_usd) AS total_revenue,
    ROUND(AVG(purchase_amount_usd), 2) AS average_order_value,
    ROUND(AVG(review_rating), 2) AS average_rating
FROM customer_shopping
GROUP BY discount_applied
ORDER BY total_revenue DESC;


-- =========================================================
-- QUERY 14: Revenue by Season
-- =========================================================

SELECT
    season,
    COUNT(*) AS total_orders,
    SUM(purchase_amount_usd) AS total_revenue,
    ROUND(AVG(purchase_amount_usd), 2) AS average_order_value
FROM customer_shopping
GROUP BY season
ORDER BY total_revenue DESC;


-- =========================================================
-- QUERY 15: Payment Method Analysis
-- =========================================================

SELECT
    payment_method,
    COUNT(*) AS total_orders,
    SUM(purchase_amount_usd) AS total_revenue,
    ROUND(AVG(purchase_amount_usd), 2) AS average_order_value
FROM customer_shopping
GROUP BY payment_method
ORDER BY total_revenue DESC;


-- =========================================================
-- QUERY 16: Subscription Adoption by Gender
-- =========================================================

SELECT
    gender,
    subscription_status,
    COUNT(*) AS customer_count
FROM customer_shopping
GROUP BY gender, subscription_status
ORDER BY gender, customer_count DESC;


-- =========================================================
-- QUERY 17: Subscription Rate by Gender
-- =========================================================

SELECT
    gender,
    COUNT(*) AS total_customers,
    SUM(subscription_status = 'Yes') AS subscribers,
    ROUND(
        100.0 * SUM(subscription_status = 'Yes') / COUNT(*),
        2
    ) AS subscription_rate
FROM customer_shopping
GROUP BY gender
ORDER BY subscription_rate DESC;


-- =========================================================
-- QUERY 18: Customer Segment Summary
-- =========================================================

SELECT
    CASE
        WHEN previous_purchases = 1 THEN 'New'
        WHEN previous_purchases BETWEEN 2 AND 10 THEN 'Returning'
        ELSE 'Loyal'
    END AS customer_segment,
    COUNT(*) AS customer_count,
    ROUND(AVG(purchase_amount_usd), 2) AS average_order_value,
    SUM(purchase_amount_usd) AS total_revenue,
    ROUND(AVG(previous_purchases), 2) AS average_previous_purchases
FROM customer_shopping
GROUP BY
    CASE
        WHEN previous_purchases = 1 THEN 'New'
        WHEN previous_purchases BETWEEN 2 AND 10 THEN 'Returning'
        ELSE 'Loyal'
    END
ORDER BY total_revenue DESC;


-- =========================================================
-- QUERY 19: Revenue by Location
-- =========================================================

SELECT
    location,
    COUNT(*) AS total_orders,
    SUM(purchase_amount_usd) AS total_revenue,
    ROUND(AVG(purchase_amount_usd), 2) AS average_order_value
FROM customer_shopping
GROUP BY location
ORDER BY total_revenue DESC;


-- =========================================================
-- QUERY 20: Top 10 Products by Revenue
-- =========================================================

SELECT
    item_purchased,
    COUNT(*) AS total_orders,
    SUM(purchase_amount_usd) AS total_revenue,
    ROUND(AVG(purchase_amount_usd), 2) AS average_order_value,
    ROUND(AVG(review_rating), 2) AS average_rating
FROM customer_shopping
GROUP BY item_purchased
ORDER BY total_revenue DESC
LIMIT 10;


-- =========================================================
-- QUERY 21: Customers with High Purchase History
-- =========================================================

SELECT
    customer_id,
    previous_purchases,
    purchase_amount_usd,
    subscription_status,
    item_purchased,
    category
FROM customer_shopping
WHERE previous_purchases >= 40
ORDER BY previous_purchases DESC,
         purchase_amount_usd DESC;


-- =========================================================
-- QUERY 22: Discount Usage by Category
-- =========================================================

SELECT
    category,
    COUNT(*) AS total_orders,
    SUM(discount_applied = 'Yes') AS discounted_orders,
    ROUND(
        100.0 * SUM(discount_applied = 'Yes') / COUNT(*),
        2
    ) AS discount_usage_percentage
FROM customer_shopping
GROUP BY category
ORDER BY discount_usage_percentage DESC;


-- =========================================================
-- QUERY 23: Revenue by Purchase Frequency
-- =========================================================

SELECT
    purchase_frequency_days,
    COUNT(*) AS total_orders,
    SUM(purchase_amount_usd) AS total_revenue,
    ROUND(AVG(purchase_amount_usd), 2) AS average_order_value
FROM customer_shopping
GROUP BY purchase_frequency_days
ORDER BY purchase_frequency_days;


-- =========================================================
-- QUERY 24: Repeat Buyers by Age Group
-- =========================================================

SELECT
    age_group,
    COUNT(*) AS repeat_buyers,
    SUM(purchase_amount_usd) AS total_revenue,
    ROUND(AVG(purchase_amount_usd), 2) AS average_order_value
FROM customer_shopping
WHERE previous_purchases > 1
GROUP BY age_group
ORDER BY repeat_buyers DESC;


-- =========================================================
-- QUERY 25: Category Performance by Subscription Status
-- =========================================================

SELECT
    category,
    subscription_status,
    COUNT(*) AS total_orders,
    SUM(purchase_amount_usd) AS total_revenue,
    ROUND(AVG(purchase_amount_usd), 2) AS average_order_value
FROM customer_shopping
GROUP BY category, subscription_status
ORDER BY category, total_revenue DESC;