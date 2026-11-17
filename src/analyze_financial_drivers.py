
from pathlib import Path
import pandas as pd

# ============================================================
# 1. PROJECT PATHS
# ============================================================

root = Path(__file__).resolve().parent.parent
processed = root / "data" / "processed"

financial_file = processed / "hospital_financial_model.csv"
peer_file = processed / "ky_large_hospital_peers.csv"

# ============================================================
# 2. LOAD DATA
# ============================================================

financials = pd.read_csv(
    financial_file,
    dtype={"provider_ccn": "string"}
)

peers = pd.read_csv(
    peer_file,
    dtype={"provider_ccn": "string"}
)

print("\nDATA LOADED")
print(f"Original financial records: {len(financials):,}")
print(f"Peer hospital records: {len(peers):,}")

# ============================================================
# 3. STANDARDIZE REPORTING DATES
# ============================================================

# The peer dataset contains fiscal_year_end,
# but does not contain fiscal_year_start.

financials["fiscal_year_end"] = pd.to_datetime(
    financials["fiscal_year_end"],
    errors="coerce"
)

peers["fiscal_year_end"] = pd.to_datetime(
    peers["fiscal_year_end"],
    errors="coerce"
)


# ============================================================
# 4. VALIDATE MATCHING KEYS
# ============================================================

merge_keys = [
    "provider_ccn",
    "fiscal_year_end"
]

# Make sure every peer has a valid identifier and dates
if peers[merge_keys].isna().any().any():
    raise ValueError(
        "Peer data contains missing provider IDs or dates."
    )

# Confirm peer records are unique
if peers.duplicated(merge_keys).any():
    raise ValueError(
        "Duplicate provider/reporting-period records found "
        "in the peer dataset."
    )

# Check the original financial dataset for ambiguous matches
source_duplicates = financials[
    financials.duplicated(merge_keys, keep=False)
].copy()

print("\nSOURCE DATA VALIDATION")
print(
    "Repeated provider/reporting-period records:",
    len(source_duplicates)
)

# Only examine source records relevant to the peer group
peer_keys = peers[merge_keys].copy()

matching_source = financials.merge(
    peer_keys,
    on=merge_keys,
    how="inner"
)

# Check whether selected peers match multiple source records
ambiguous_matches = matching_source[
    matching_source.duplicated(
        merge_keys,
        keep=False
    )
]

if not ambiguous_matches.empty:
    output = processed / "ambiguous_peer_matches.csv"

    ambiguous_matches.to_csv(
        output,
        index=False
    )

    raise ValueError(
        f"Ambiguous source records found. Review {output}"
    )

# ============================================================
# 5. MERGE PEER HOSPITALS WITH FINANCIAL DATA
# ============================================================

df = peers[merge_keys].merge(
    matching_source,
    on=merge_keys,
    how="left",
    validate="one_to_one",
    indicator=True
)

# Verify every peer matched successfully
unmatched = df[df["_merge"] != "both"]

if not unmatched.empty:
    output = processed / "unmatched_peer_records.csv"

    unmatched.to_csv(
        output,
        index=False
    )

    raise ValueError(
        f"Some peer hospitals did not match. Review {output}"
    )

df = df.drop(columns=["_merge"])

print("\nMERGE VALIDATION")
print(f"Successfully matched hospitals: {len(df):,}")

# ============================================================
# 6. CALCULATE FINANCIAL METRICS
# ============================================================

# Ensure required fields are numeric
numeric_columns = [
    "net_patient_revenue",
    "operating_expense",
    "total_salaries",
    "patient_days"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

# Prevent division by zero or invalid denominators
valid_revenue = df["net_patient_revenue"].where(
    df["net_patient_revenue"] > 0
)

valid_expense = df["operating_expense"].where(
    df["operating_expense"] > 0
)

valid_days = df["patient_days"].where(
    df["patient_days"] > 0
)

# Operating income
df["operating_income"] = (
    df["net_patient_revenue"]
    - df["operating_expense"]
)

# Operating margin
df["operating_margin_pct"] = (
    df["operating_income"] / valid_revenue
) * 100

# Expense as a percentage of revenue
df["expense_ratio_pct"] = (
    df["operating_expense"] / valid_revenue
) * 100

# Salary expense as a percentage of revenue
df["salary_to_revenue_pct"] = (
    df["total_salaries"] / valid_revenue
) * 100

# Salary expense as a percentage of operating expense
df["salary_to_expense_pct"] = (
    df["total_salaries"] / valid_expense
) * 100

# Revenue per reported inpatient day
df["revenue_per_patient_day"] = (
    df["net_patient_revenue"] / valid_days
)

# Operating expense per reported inpatient day
df["expense_per_patient_day"] = (
    df["operating_expense"] / valid_days
)

# ============================================================
# 7. CREATE FINAL ANALYSIS DATASET
# ============================================================

results = df[
    [
        "provider_ccn",
        "hospital_name",
        "fiscal_year_start",
        "fiscal_year_end",
        "net_patient_revenue",
        "operating_expense",
        "operating_income",
        "total_salaries",
        "patient_days",
        "operating_margin_pct",
        "expense_ratio_pct",
        "salary_to_revenue_pct",
        "salary_to_expense_pct",
        "revenue_per_patient_day",
        "expense_per_patient_day"
    ]
].copy()

results = results.sort_values(
    "operating_margin_pct"
)

# ============================================================
# 8. SAVE RESULTS
# ============================================================

output = processed / "financial_driver_analysis.csv"

results.to_csv(
    output,
    index=False
)

# ============================================================
# 9. DISPLAY RESULTS
# ============================================================

print("\nFINANCIAL DRIVER ANALYSIS")

display_columns = [
    "hospital_name",
    "operating_margin_pct",
    "expense_ratio_pct",
    "salary_to_revenue_pct",
    "salary_to_expense_pct",
    "revenue_per_patient_day",
    "expense_per_patient_day"
]

print(
    results[display_columns]
    .round(2)
    .to_string(index=False)
)

print("\nMISSING VALUES BY METRIC")

print(
    results[display_columns]
    .isna()
    .sum()
    .to_string()
)

print("\nFINANCIAL SUMMARY")

print(
    "Median operating margin:",
    round(results["operating_margin_pct"].median(), 2),
    "%"
)

print(
    "Median expense ratio:",
    round(results["expense_ratio_pct"].median(), 2),
    "%"
)

print("\nSaved to:", output)

print("\nFinancial driver analysis complete!")
