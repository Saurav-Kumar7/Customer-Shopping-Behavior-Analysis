"""
Customer Shopping Behavior Analysis
------------------------------------
Cleans, transforms, and validates the raw customer shopping dataset
before loading it into MySQL.
"""

from pathlib import Path

import pandas as pd


def load_data(file_path: Path) -> pd.DataFrame:
    """Load the raw customer shopping dataset."""
    if not file_path.exists():
        raise FileNotFoundError(
            f"Input dataset not found: {file_path}"
        )

    return pd.read_csv(file_path)


def clean_review_ratings(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing review ratings using category-level medians."""
    missing_before = df["Review Rating"].isna().sum()

    print(f"Missing Review Ratings BEFORE cleaning: {missing_before}")

    category_medians = (
        df.groupby("Category")["Review Rating"]
        .transform("median")
    )

    df["Review Rating"] = df["Review Rating"].fillna(category_medians)

    missing_after = df["Review Rating"].isna().sum()

    print(f"Missing Review Ratings AFTER cleaning: {missing_after}")

    print("\nMedian Review Rating by Category:")
    print(
        df.groupby("Category")["Review Rating"]
        .median()
    )

    return df


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names for easier analysis and SQL usage."""
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
        .str.replace(r"[()]", "", regex=True)
    )

    print("\nStandardized Column Names:")
    print(df.columns.tolist())

    return df


def create_age_groups(df: pd.DataFrame) -> pd.DataFrame:
    """Create customer age groups for demographic analysis."""
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 25, 35, 45, 55, 100],
        labels=[
            "18-25",
            "26-35",
            "36-45",
            "46-55",
            "56+",
        ],
    )

    print("\nAge Group Distribution:")
    print(df["age_group"].value_counts().sort_index())

    return df


def create_purchase_frequency_days(df: pd.DataFrame) -> pd.DataFrame:
    """Convert purchase frequency categories into approximate days."""
    frequency_mapping = {
        "Weekly": 7,
        "Fortnightly": 14,
        "Bi-Weekly": 14,
        "Monthly": 30,
        "Quarterly": 90,
        "Every 3 Months": 90,
        "Annually": 365,
    }

    df["purchase_frequency_days"] = (
        df["frequency_of_purchases"].map(frequency_mapping)
    )

    unmapped_values = (
        df.loc[
            df["purchase_frequency_days"].isna(),
            "frequency_of_purchases",
        ]
        .dropna()
        .unique()
    )

    if len(unmapped_values) > 0:
        raise ValueError(
            "Unexpected purchase frequency values found: "
            f"{list(unmapped_values)}"
        )

    print("\nPurchase Frequency Mapping:")
    print(
        df[
            [
                "frequency_of_purchases",
                "purchase_frequency_days",
            ]
        ]
        .drop_duplicates()
        .sort_values("purchase_frequency_days")
    )

    return df


def remove_redundant_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Check and remove redundant promotional columns."""
    print("\nDiscount Applied vs Promo Code Used:")

    discount_promo_check = pd.crosstab(
        df["discount_applied"],
        df["promo_code_used"],
    )

    print(discount_promo_check)

    df = df.drop(columns=["promo_code_used"])

    print("\nColumn removed: promo_code_used")

    return df


def validate_data(df: pd.DataFrame) -> None:
    """Run final data-quality checks on the cleaned dataset."""
    print("\n" + "=" * 60)
    print("FINAL DATA QUALITY VALIDATION")
    print("=" * 60)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nFinal Dataset Shape:")
    print(df.shape)

    print("\nAge Range:")
    print(f"{df['age'].min()} to {df['age'].max()}")

    print("\nPurchase Amount Range:")
    print(
        f"{df['purchase_amount_usd'].min()} "
        f"to {df['purchase_amount_usd'].max()}"
    )

    print("\nReview Rating Range:")
    print(
        f"{df['review_rating'].min()} "
        f"to {df['review_rating'].max()}"
    )

    print("\nAge Groups:")
    print(df["age_group"].value_counts().sort_index())

    print("\nPurchase Frequency Days:")
    print(
        df["purchase_frequency_days"]
        .value_counts()
        .sort_index()
    )


def save_cleaned_data(df: pd.DataFrame, file_path: Path) -> None:
    """Save the cleaned dataset to CSV."""
    df.to_csv(file_path, index=False)

    print("\nCleaned dataset saved successfully!")
    print(f"File location: {file_path}")


def main() -> None:
    """Run the complete data-cleaning pipeline."""
    project_root = Path(__file__).resolve().parent.parent

    raw_file_path = (
        project_root
        / "data"
        / "customer_shopping_behavior.csv"
    )

    cleaned_file_path = (
        project_root
        / "data"
        / "customer_shopping_behavior_cleaned.csv"
    )

    df = load_data(raw_file_path)

    df = clean_review_ratings(df)
    df = standardize_column_names(df)
    df = create_age_groups(df)
    df = create_purchase_frequency_days(df)
    df = remove_redundant_columns(df)

    validate_data(df)
    save_cleaned_data(df, cleaned_file_path)


if __name__ == "__main__":
    main()