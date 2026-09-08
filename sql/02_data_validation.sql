USE customer_shopping_analysis;


-- ============================================================
-- 1. TOTAL RECORD COUNT
-- ============================================================

SELECT COUNT(*) AS total_records
FROM customer_shopping;


-- ============================================================
-- 2. CHECK FOR DUPLICATE CUSTOMER IDs
-- ============================================================

SELECT
    customer_id,
    COUNT(*) AS record_count
FROM customer_shopping
GROUP BY customer_id
HAVING COUNT(*) > 1;


-- ============================================================
-- 3. CHECK FOR MISSING VALUES
-- ============================================================

SELECT
    COUNT(*) AS total_records,
    SUM(customer_id IS NULL) AS missing_customer_id,
    SUM(age IS NULL) AS missing_age,
    SUM(gender IS NULL) AS missing_gender,
    SUM(item_purchased IS NULL) AS missing_item,
    SUM(category IS NULL) AS missing_category,
    SUM(purchase_amount_usd IS NULL) AS missing_purchase_amount,
    SUM(location IS NULL) AS missing_location,
    SUM(size IS NULL) AS missing_size,
    SUM(color IS NULL) AS missing_color,
    SUM(season IS NULL) AS missing_season,
    SUM(review_rating IS NULL) AS missing_rating,
    SUM(subscription_status IS NULL) AS missing_subscription,
    SUM(shipping_type IS NULL) AS missing_shipping,
    SUM(discount_applied IS NULL) AS missing_discount,
    SUM(previous_purchases IS NULL) AS missing_previous_purchases,
    SUM(payment_method IS NULL) AS missing_payment_method,
    SUM(frequency_of_purchases IS NULL) AS missing_frequency,
    SUM(age_group IS NULL) AS missing_age_group,
    SUM(purchase_frequency_days IS NULL) AS missing_frequency_days
FROM customer_shopping;


-- ============================================================
-- 4. CHECK NUMERIC RANGES
-- ============================================================

SELECT
    MIN(age) AS minimum_age,
    MAX(age) AS maximum_age,
    MIN(purchase_amount_usd) AS minimum_purchase,
    MAX(purchase_amount_usd) AS maximum_purchase,
    MIN(review_rating) AS minimum_rating,
    MAX(review_rating) AS maximum_rating,
    MIN(previous_purchases) AS minimum_previous_purchases,
    MAX(previous_purchases) AS maximum_previous_purchases
FROM customer_shopping;


-- ============================================================
-- 5. CHECK AGE GROUP DISTRIBUTION
-- ============================================================

SELECT
    age_group,
    COUNT(*) AS customer_count
FROM customer_shopping
GROUP BY age_group
ORDER BY customer_count DESC;


-- ============================================================
-- 6. CHECK PURCHASE FREQUENCY DAYS
-- ============================================================

SELECT
    purchase_frequency_days,
    COUNT(*) AS customer_count
FROM customer_shopping
GROUP BY purchase_frequency_days
ORDER BY purchase_frequency_days;