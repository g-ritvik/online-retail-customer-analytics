
import pandas as pd
from pathlib import Path


# ============================================================
# Project paths and configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA = DATA_DIR / "raw_online_retail_II.csv"

PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_PATH = PROCESSED_DIR / "online_retail_cleaned.csv"


# ============================================================
# Console output helpers
# ============================================================

def print_section(title: str) -> None:
    """Print a consistent section heading."""
    print(f"\n{'=' * 60}")
    print(title.upper())
    print(f"{'=' * 60}")


def print_status(message: str, status: str = "PASS") -> None:
    """Print a concise pipeline status message."""
    print(f"[{status}] {message}")


# ============================================================
# Data loading and standardization
# ============================================================

def load_data(file_path: Path) -> pd.DataFrame:
    """Load the raw transaction dataset."""
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    df = pd.read_csv(file_path)

    if df.empty:
        raise ValueError("The raw dataset is empty.")

    print_status(
        f"Loaded {len(df):,} records and {len(df.columns)} columns."
    )

    return df


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Convert column names to lowercase snake_case."""
    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
    )

    print_status("Column names standardized.")

    return df


def standardize_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Convert date and identifier columns to appropriate data types."""
    df = df.copy()

    df["invoicedate"] = pd.to_datetime(
        df["invoicedate"],
        errors="raise"
    )

    df["customer_id"] = (
        df["customer_id"]
        .astype("Int64")
        .astype("string")
    )

    print_status("Date and identifier data types standardized.")

    return df


# ============================================================
# Missing-value treatment
# ============================================================

def assess_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize missing values across all columns."""
    missing_summary = pd.DataFrame({
        "missing_count": df.isna().sum(),
        "missing_percentage": (df.isna().mean() * 100).round(2)
    })

    missing_summary = missing_summary[
        missing_summary["missing_count"] > 0
    ]

    print_section("Missing Value Assessment")

    if missing_summary.empty:
        print_status("No missing values detected.")
    else:
        print(missing_summary.to_string())

    return missing_summary


def recover_missing_descriptions(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing descriptions using unambiguous StockCode matches."""
    df = df.copy()

    description_mapping = (
        df.dropna(subset=["description"])
        .groupby("stockcode")["description"]
        .agg(
            lambda values: (
                values.unique()[0]
                if values.nunique() == 1
                else pd.NA
            )
        )
        .dropna()
    )

    missing_before = df["description"].isna().sum()

    df["description"] = df["description"].fillna(
        df["stockcode"].map(description_mapping)
    )

    recovered = missing_before - df["description"].isna().sum()
    remaining = df["description"].isna().sum()

    print_section("Description Recovery")
    print_status(f"Descriptions recovered: {recovered:,}")
    print_status(f"Descriptions remaining missing: {remaining:,}")

    return df


# ============================================================
# Duplicate treatment
# ============================================================

def remove_exact_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove fully identical duplicate records."""
    initial_count = len(df)

    df = df.drop_duplicates().copy()

    removed_count = initial_count - len(df)

    print_section("Exact Duplicate Removal")
    print_status(f"Duplicate records removed: {removed_count:,}")
    print_status(f"Records remaining: {len(df):,}")

    return df


def inspect_repeated_combinations(df: pd.DataFrame) -> None:
    """Report repeated invoice, quantity, and StockCode combinations."""

    repeated = df[
        df.duplicated(
            subset=["invoice", "quantity", "stockcode"],
            keep=False
        )
    ]

    differences = (
        repeated
        .groupby(["invoice", "quantity", "stockcode"])[
            ["price", "invoicedate", "description", "customer_id", "country"]
        ]
        .nunique(dropna=False)
    )

    print_section("Repeated Transaction Investigation")
    print(f"Records involved: {len(repeated):,}")

    if repeated.empty:
        print_status("No repeated transaction combinations found.")
        return

    difference_counts = differences.gt(1).sum()

    print("\nGroups with differences by field:")
    print(difference_counts.to_string())


# ============================================================
# Transaction investigation and classification
# ============================================================

def assess_transaction_values(df: pd.DataFrame) -> None:
    """Summarize unusual quantity and price values."""

    print_section("Transaction Value Assessment")

    checks = {
        "Negative quantities": df["quantity"] < 0,
        "Zero quantities": df["quantity"] == 0,
        "Positive quantities": df["quantity"] > 0,
        "Negative prices": df["price"] < 0,
        "Zero prices": df["price"] == 0,
        "Positive prices": df["price"] > 0,
    }

    for label, condition in checks.items():
        print(f"{label:<25}: {condition.sum():>10,}")

    print("\nInvoice prefix counts:")
    print(
        df["invoice"]
        .str[0]
        .value_counts(dropna=False)
        .sort_index()
        .to_string()
    )

    print("\nSpecial StockCode counts (alphabetic codes only):")
    special_codes = (
        df[df["stockcode"].str.fullmatch(r"[A-Za-z]+", na=False)]
        ["stockcode"]
        .value_counts()
        .head(20)
    )

    if special_codes.empty:
        print("No matching codes found.")
    else:
        print(special_codes.to_string())


def classify_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Add transaction-type indicators without removing records."""
    df = df.copy()

    invoice_prefix = df["invoice"].str[0].str.upper()

    df["is_cancellation"] = invoice_prefix.eq("C")
    df["is_adjustment"] = invoice_prefix.eq("A")

    df["is_negative_quantity"] = df["quantity"] < 0
    df["is_zero_quantity"] = df["quantity"] == 0

    df["is_negative_price"] = df["price"] < 0
    df["is_zero_price"] = df["price"] == 0

    print_status("Transaction classification flags created.")

    return df


# ============================================================
# Derived variables
# ============================================================

def construct_variables(df: pd.DataFrame) -> pd.DataFrame:
    """Construct transaction-level analytical variables."""
    df = df.copy()

    df["line_value"] = df["quantity"] * df["price"]

    print_status("Line value variable constructed.")

    return df


# ============================================================
# Export and final validation
# ============================================================

def validate_cleaned_data(df: pd.DataFrame) -> None:
    """Run final quality checks on the cleaned dataset."""

    print_section("Final Data Validation")

    checks = {
        "Exact duplicate records": df.duplicated().sum(),
        "Missing customer IDs": df["customer_id"].isna().sum(),
        "Missing descriptions": df["description"].isna().sum(),
        "Missing invoice dates": df["invoicedate"].isna().sum(),
        "Missing line values": df["line_value"].isna().sum(),
    }

    print(f"Total records : {len(df):,}")
    print(f"Total columns : {len(df.columns):,}")

    for label, count in checks.items():
        print(f"{label:<28}: {count:>10,}")

    if df["invoicedate"].isna().any():
        raise ValueError("Missing invoice dates found.")

    if df["line_value"].isna().any():
        raise ValueError("Missing line values found.")

    print_status("Required validation checks passed.")

    print("\nFinal data types:")
    print(df.dtypes.to_string())


def export_cleaned_data(df: pd.DataFrame, file_path: Path) -> None:
    """Export the cleaned dataset to CSV."""
    file_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(file_path, index=False)

    file_size = file_path.stat().st_size / (1024 ** 2)

    print_section("Data Export")
    print_status("Cleaned dataset exported successfully.")
    print(f"Output file : {file_path}")
    print(f"File size   : {file_size:.2f} MB")


# ============================================================
# Main execution
# ============================================================

def main() -> None:
    print_section("Online Retail II Data Cleaning Pipeline")
    print("[START] Beginning data preparation.")

    # Load and standardize
    print_section("Data Loading and Standardization")

    df = load_data(RAW_DATA)
    df = standardize_column_names(df)
    df = standardize_data_types(df)

    print("\nStandardized data types:")
    print(df.dtypes.to_string())

    # Missing-value treatment
    assess_missing_values(df)
    df = recover_missing_descriptions(df)

    # Duplicate treatment
    df = remove_exact_duplicates(df)
    inspect_repeated_combinations(df)

    # Transaction investigation and classification
    assess_transaction_values(df)
    df = classify_transactions(df)

    # Derived variables
    print_section("Variable Construction")
    df = construct_variables(df)

    # Final validation and export
    validate_cleaned_data(df)
    export_cleaned_data(df, OUTPUT_PATH)

    print_section("Pipeline Execution Summary")
    print_status("Data cleaning pipeline completed successfully.")
    print(f"Final dataset: {len(df):,} records × {len(df.columns)} columns")


if __name__ == "__main__":
    main()
