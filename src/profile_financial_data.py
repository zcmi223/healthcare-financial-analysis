
from pathlib import Path
import pandas as pd

# Locate the CMS dataset
project_root = Path(__file__).resolve().parent.parent
raw_folder = project_root / "data" / "raw"

csv_files = list(raw_folder.glob("*.csv"))

if len(csv_files) != 1:
    raise RuntimeError(
        f"Expected one CSV in data/raw, found {len(csv_files)}."
    )

df = pd.read_csv(csv_files[0], low_memory=False)

print("\nDATASET SIZE")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns):,}")

# Identify columns potentially related to financial analysis
keywords = [
    "revenue",
    "expense",
    "income",
    "salary",
    "cost",
    "profit",
    "patient",
    "medicare",
    "provider",
    "state",
    "year"
]

matching_columns = [
    col for col in df.columns
    if any(word in col.lower() for word in keywords)
]

print("\nPOTENTIAL FINANCIAL AND IDENTIFIER COLUMNS")
for col in matching_columns:
    print(col)

print("\nCOLUMN DATA TYPES")
print(df[matching_columns].dtypes.to_string())

# Save a complete column inventory for review
inventory = pd.DataFrame({
    "column_name": df.columns,
    "data_type": df.dtypes.astype(str).values,
    "non_null_count": df.notna().sum().values,
    "missing_pct": (
        df.isna().mean().values * 100
    ).round(2)
})

output_folder = project_root / "data" / "processed"
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "column_inventory.csv"
inventory.to_csv(output_file, index=False)

print(f"\nColumn inventory saved to: {output_file}")
print("\nFinancial data profiling complete!")
