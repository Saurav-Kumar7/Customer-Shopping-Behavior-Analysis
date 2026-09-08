import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. LOAD DATA
# --------------------------------------------------

project_root = Path(__file__).resolve().parent.parent

file_path = project_root / "data" / "customer_shopping_behavior.csv"

df = pd.read_csv(file_path)


# --------------------------------------------------
# 2. CHECK MISSING REVIEW RATINGS
# --------------------------------------------------

print("Missing Review Ratings BEFORE cleaning:")
print(df["Review Rating"].isnull().sum())


# --------------------------------------------------
# 3. CALCULATE MEDIAN RATING BY CATEGORY
# --------------------------------------------------

category_medians = df.groupby("Category")["Review Rating"].transform("median")


# --------------------------------------------------
# 4. FILL MISSING RATINGS
# --------------------------------------------------

df["Review Rating"] = df["Review Rating"].fillna(category_medians)


# --------------------------------------------------
# 5. VERIFY CLEANING
# --------------------------------------------------

print("\nMissing Review Ratings AFTER cleaning:")
print(df["Review Rating"].isnull().sum())


# --------------------------------------------------
# 6. DISPLAY CATEGORY MEDIANS
# --------------------------------------------------

print("\nMedian Review Rating by Category:")
print(
    df.groupby("Category")["Review Rating"]
    .median()
)

# --------------------------------------------------
# 7. STANDARDIZE COLUMN NAMES
# --------------------------------------------------

df.columns = (
    df.columns
    .str.lower()
    .str.strip()
    .str.replace(" ", "_")
    .str.replace(r"[()]", "", regex=True)
)

print("\nStandardized Column Names:")
print(df.columns.tolist())


# --------------------------------------------------
# 8. CREATE AGE GROUP
# --------------------------------------------------

df["age_group"] = pd.cut(
    df["age"],
    bins=[0, 25, 35, 45, 55, 100],
    labels=[
        "18-25",
        "26-35",
        "36-45",
        "46-55",
        "56+"
    ]
)

print("\nAge Group Distribution:")
print(df["age_group"].value_counts().sort_index())


# --------------------------------------------------
# 9. CREATE PURCHASE FREQUENCY IN DAYS
# --------------------------------------------------

frequency_mapping = {
    "Weekly": 7,
    "Fortnightly": 14,
    "Bi-Weekly": 14,
    "Monthly": 30,
    "Quarterly": 90,
    "Every 3 Months": 90,
    "Annually": 365
}

df["purchase_frequency_days"] = (
    df["frequency_of_purchases"]
    .map(frequency_mapping)
)

print("\nPurchase Frequency Mapping:")
print(
    df[
        [
            "frequency_of_purchases",
            "purchase_frequency_days"
        ]
    ].drop_duplicates()
    .sort_values("purchase_frequency_days")
)


# --------------------------------------------------
# 10. CHECK DISCOUNT AND PROMO CODE RELATIONSHIP
# --------------------------------------------------

print("\nDiscount Applied vs Promo Code Used:")

discount_promo_check = pd.crosstab(
    df["discount_applied"],
    df["promo_code_used"]
)

print(discount_promo_check)


# --------------------------------------------------
# 11. REMOVE REDUNDANT COLUMN
# --------------------------------------------------

df = df.drop(columns=["promo_code_used"])

print("\nColumn removed: promo_code_used")

print("\nColumns after removing redundant column:")
print(df.columns.tolist())


# --------------------------------------------------
# 12. FINAL DATA QUALITY VALIDATION
# --------------------------------------------------

print("\n" + "=" * 60)
print("FINAL DATA QUALITY VALIDATION")
print("=" * 60)

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Check duplicate rows
print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Check dataset shape
print("\nFinal Dataset Shape:")
print(df.shape)

# Check age range
print("\nAge Range:")
print(df["age"].min(), "to", df["age"].max())

# Check purchase amount range
print("\nPurchase Amount Range:")
print(
    df["purchase_amount_usd"].min(),
    "to",
    df["purchase_amount_usd"].max()
)

# Check review rating range
print("\nReview Rating Range:")
print(
    df["review_rating"].min(),
    "to",
    df["review_rating"].max()
)

# Check derived age groups
print("\nAge Groups:")
print(df["age_group"].value_counts().sort_index())

# Check purchase frequency mapping
print("\nPurchase Frequency Days:")
print(
    df["purchase_frequency_days"]
    .value_counts()
    .sort_index()
)


# --------------------------------------------------
# 13. SAVE CLEANED DATASET
# --------------------------------------------------

cleaned_file_path = (
    project_root
    / "data"
    / "customer_shopping_behavior_cleaned.csv"
)

df.to_csv(cleaned_file_path, index=False)

print("\nCleaned dataset saved successfully!")
print(f"File location: {cleaned_file_path}")