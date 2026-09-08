-- ============================================================
-- CUSTOMER SHOPPING BEHAVIOR ANALYSIS
-- MySQL Database Setup
-- ============================================================

CREATE DATABASE IF NOT EXISTS customer_shopping_analysis;

USE customer_shopping_analysis;

-- Remove existing table if rerunning the script
DROP TABLE IF EXISTS customer_shopping;

-- Create main customer shopping table
CREATE TABLE customer_shopping (
    customer_id INT PRIMARY KEY,
    age INT,
    gender VARCHAR(20),
    item_purchased VARCHAR(100),
    category VARCHAR(50),
    purchase_amount_usd DECIMAL(10,2),
    location VARCHAR(100),
    size VARCHAR(10),
    color VARCHAR(50),
    season VARCHAR(20),
    review_rating DECIMAL(3,1),
    subscription_status VARCHAR(20),
    shipping_type VARCHAR(50),
    discount_applied VARCHAR(10),
    previous_purchases INT,
    payment_method VARCHAR(50),
    frequency_of_purchases VARCHAR(50),
    age_group VARCHAR(20),
    purchase_frequency_days INT
);