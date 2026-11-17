
from pathlib import Path
import pandas as pd

# Locate the project's raw data folder
project_root = Path(__file__).resolve().parent.parent
raw_folder = project_root / "data" / "raw"

# Find downloaded CSV files
csv_files = list(raw_folder.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError(
        "No CSV file found in data/raw. Download the CMS dataset first."
    )

if len(csv_files) > 1:
    raise RuntimeError(
        "Multiple CSV files found. Keep only the 2024 CMS file "
        "in data/raw for this first test."
    )

file_path = csv_files[0]

# Load the hospital data
df = pd.read_csv(file_path, low_memory=False)

print("\nFILE:", file_path.name)
print("\nDATASET SHAPE:", df.shape)

print("\nFIRST FIVE ROWS:")
print(df.head().to_string())

print("\nCOLUMN NAMES:")
for column in df.columns:
    print(column)

print("\nMISSING VALUES (TOP 15):")
print(df.isna().sum().sort_values(ascending=False).head(15))

print("\nData exploration complete!")
