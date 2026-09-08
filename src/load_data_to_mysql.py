import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv
from pathlib import Path


# --------------------------------------------------
# 1. PROJECT PATH
# --------------------------------------------------

project_root = Path(__file__).resolve().parent.parent

cleaned_file_path = (
    project_root
    / "data"
    / "customer_shopping_behavior_cleaned.csv"
)


# --------------------------------------------------
# 2. LOAD CLEANED CSV
# --------------------------------------------------

df = pd.read_csv(cleaned_file_path)

print("Cleaned CSV loaded successfully!")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")


# --------------------------------------------------
# 3. CONNECT TO MYSQL
# --------------------------------------------------
load_dotenv()
connection = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password=os.getenv("MYSQL_PASSWORD"),
    database="customer_shopping_analysis"
)

cursor = connection.cursor()

print("Connected to MySQL successfully!")


# --------------------------------------------------
# 4. INSERT DATA
# --------------------------------------------------

insert_query = """
INSERT INTO customer_shopping (
    customer_id,
    age,
    gender,
    item_purchased,
    category,
    purchase_amount_usd,
    location,
    size,
    color,
    season,
    review_rating,
    subscription_status,
    shipping_type,
    discount_applied,
    previous_purchases,
    payment_method,
    frequency_of_purchases,
    age_group,
    purchase_frequency_days
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
"""


data = [
    tuple(row)
    for row in df.itertuples(index=False, name=None)
]


cursor.executemany(insert_query, data)

connection.commit()

print(f"{cursor.rowcount} rows inserted successfully!")


# --------------------------------------------------
# 5. CLOSE CONNECTION
# --------------------------------------------------

cursor.close()
connection.close()

print("MySQL connection closed.")
print("Data loading completed successfully!")