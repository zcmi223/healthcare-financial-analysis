
from pathlib import Path
import pandas as pd

root = Path(__file__).resolve().parent.parent
raw = root / "data" / "raw"
processed = root / "data" / "processed"

# Load national teaching-hospital benchmark
peers = pd.read_csv(
    processed / "national_teaching_hospitals.csv",
    dtype={"ccn": "string"}
)

# Load original CMS financial data
files = list(raw.glob("*.csv"))
if len(files) != 1:
    raise ValueError("Expected one CMS CSV in data/raw")

cms = pd.read_csv(
    files[0],
    low_memory=False,
    dtype={"Provider CCN": "string"}
)

# Select CMS financial statement fields
columns = {
    "Provider CCN": "ccn",
    "Fiscal Year Begin Date": "start",
    "Fiscal Year End Date": "end",
    "Net Patient Revenue": "revenue",
    "Less Total Operating Expense": "expenses",
    "Net Income from Service to Patients": "service_income",
    "Total Other Income": "other_income",
    "Total Other Expenses": "other_expenses",
    "Net Income": "net_income"
}

cms = cms[list(columns)].rename(columns=columns)

# Standardize reporting identifiers
for df in [cms, peers]:
    df["ccn"] = df["ccn"].str.zfill(6)

    for col in ["start", "end"]:
        df[col] = pd.to_datetime(
            df[col], errors="coerce"
        )

keys = ["ccn", "start", "end"]

# Match the exact CMS reporting periods
matched = peers.merge(
    cms,
    on=keys,
    how="left",
    validate="one_to_one",
    indicator=True,
    suffixes=("", "_cms")
)

if (matched["_merge"] != "both").any():
    raise ValueError("Some hospital reports did not match")

# Check source revenue and expense consistency
for col in ["revenue", "expenses"]:
    matched[col] = pd.to_numeric(
        matched[col], errors="coerce"
    )

    matched[f"{col}_cms"] = pd.to_numeric(
        matched[f"{col}_cms"], errors="coerce"
    )

    difference = (
        matched[col] - matched[f"{col}_cms"]
    ).abs()

    if difference.gt(1).any():
        raise ValueError(f"Source reconciliation failed: {col}")

# Convert income fields to numeric
for col in [
    "service_income", "other_income",
    "other_expenses", "net_income"
]:
    matched[col] = pd.to_numeric(
        matched[col], errors="coerce"
    )

# Calculate financial measures
matched["service_margin_pct"] = (
    matched["service_income"]
    / matched["revenue"] * 100
)

matched["net_margin_pct"] = (
    matched["net_income"]
    / matched["revenue"] * 100
)

matched["other_income_pct"] = (
    matched["other_income"]
    / matched["revenue"] * 100
)

# Verify CMS net income calculation
matched["income_bridge_difference"] = (
    matched["service_income"]
    + matched["other_income"]
    - matched["other_expenses"]
    - matched["net_income"]
)

# Save the full national dataset
output = processed / "national_income_bridge.csv"
matched.to_csv(output, index=False)

# Focus on University Hospital
university = matched[
    matched["ccn"] == "180067"
]

print("\nUNIVERSITY HOSPITAL INCOME BRIDGE")

print(
    university[
        [
            "hospital",
            "service_income",
            "other_income",
            "other_expenses",
            "net_income",
            "service_margin_pct",
            "net_margin_pct"
        ]
    ].round(2).to_string(index=False)
)

print("\nNATIONAL COMPARISON")
print(
    "Median patient-service margin:",
    round(matched["service_margin_pct"].median(), 2)
)

print(
    "Median net margin:",
    round(matched["net_margin_pct"].median(), 2)
)

print("\nINCOME RECONCILIATION")
print(
    "Records with differences greater than $1:",
    matched["income_bridge_difference"].abs().gt(1).sum()
)

print(
    "Records with incomplete income bridge:",
    matched["income_bridge_difference"].isna().sum()
)

print("\nSaved:", output)
print("Income bridge analysis complete!")
