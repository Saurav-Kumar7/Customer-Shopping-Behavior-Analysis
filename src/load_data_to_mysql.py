"""
Customer Shopping Behavior Analysis
------------------------------------
Loads the cleaned customer shopping dataset from CSV
into the MySQL customer_shopping table.
"""

import os
from pathlib import Path

import mysql.connector
import pandas as pd
from dotenv import load_dotenv


DATABASE_NAME = "customer_shopping_analysis"
TABLE_NAME = "customer_shopping"


def load_cleaned_data(file_path: Path) -> pd.DataFrame:
    """Load the cleaned CSV dataset."""
    if not file_path.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    print("Cleaned CSV loaded successfully!")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    return df


def connect_to_mysql():
    """Create and return a MySQL database connection."""
    load_dotenv()

    mysql_password = os.getenv("MYSQL_PASSWORD")

    if not mysql_password:
        raise ValueError(
            "MYSQL_PASSWORD was not found in the environment."
        )

    connection = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password=mysql_password,
        database=DATABASE_NAME,
    )

    print("Connected to MySQL successfully!")

    return connection


def insert_data(connection, df: pd.DataFrame) -> int:
    """Insert the cleaned dataset into the MySQL table."""
    insert_query = f"""
INSERT INTO {TABLE_NAME} (
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
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

    data = [
        tuple(row)
        for row in df.itertuples(index=False, name=None)
    ]

    cursor = connection.cursor()

    try:
        cursor.executemany(insert_query, data)
        connection.commit()

        rows_inserted = cursor.rowcount

        print(f"{rows_inserted} rows inserted successfully!")

        return rows_inserted

    except mysql.connector.Error:
        connection.rollback()
        raise

    finally:
        cursor.close()


def main() -> None:
    """Run the complete CSV-to-MySQL loading pipeline."""
    project_root = Path(__file__).resolve().parent.parent

    cleaned_file_path = (
        project_root
        / "data"
        / "customer_shopping_behavior_cleaned.csv"
    )

    df = load_cleaned_data(cleaned_file_path)

    connection = None

    try:
        connection = connect_to_mysql()
        insert_data(connection, df)

        print("Data loading completed successfully!")

    except mysql.connector.Error as error:
        print(f"MySQL error: {error}")
        raise

    finally:
        if connection is not None and connection.is_connected():
            connection.close()
            print("MySQL connection closed.")


if __name__ == "__main__":
    main()