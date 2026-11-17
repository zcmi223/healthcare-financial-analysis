
from pathlib import Path
import pandas as pd

root = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    root / "data/processed/hospital_financial_model.csv",
    dtype={"provider_ccn": "string"}
)

# Calculate reporting period lengths
df["fiscal_year_start"] = pd.to_datetime(
    df["fiscal_year_start"]
)
df["fiscal_year_end"] = pd.to_datetime(
    df["fiscal_year_end"]
)

df["reporting_days"] = (
    df["fiscal_year_end"] - df["fiscal_year_start"]
).dt.days + 1

# Identify repeated providers
df["repeated_provider"] = df.duplicated(
    subset=["provider_ccn"], keep=False
)

print("\nDATA QUALITY SUMMARY")
print("Total records:", len(df))
print("Unique provider CCNs:", df["provider_ccn"].nunique())
print("Repeated-provider records:",
      df["repeated_provider"].sum())
print("Records with 350-380 reporting days:",
      df["reporting_days"].between(350, 380).sum())

# Find university hospitals in Kentucky
ky = df[df["state"] == "KY"]

matches = ky[
    ky["hospital_name"].str.contains(
        "UNIVERSITY|CHANDLER",
        case=False, na=False
    )
]

print("\nKENTUCKY UNIVERSITY HOSPITALS")
print(matches[
    [
        "provider_ccn",
        "hospital_name",
        "fiscal_year_start",
        "fiscal_year_end",
        "operating_margin_pct"
    ]
].to_string(index=False))

# Export flagged records for review
flags = df[
    df["repeated_provider"]
    | ~df["reporting_days"].between(350, 380)
]

output = root / "data/processed/data_quality_flags.csv"
flags.to_csv(output, index=False)

print("\nFlagged records saved:", output)
print("\nValidation complete!")
