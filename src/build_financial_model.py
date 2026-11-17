
from pathlib import Path
import pandas as pd

# Project folders
root = Path(__file__).resolve().parent.parent
raw = root / "data" / "raw"
processed = root / "data" / "processed"
processed.mkdir(parents=True, exist_ok=True)

# Load CMS hospital cost report
files = list(raw.glob("*.csv"))

if len(files) != 1:
    raise RuntimeError(
        f"Expected one CSV in data/raw, found {len(files)}"
    )

df = pd.read_csv(files[0], low_memory=False)

# Select financial and hospital identifier columns
columns = {
    "Provider CCN": "provider_ccn",
    "Hospital Name": "hospital_name",
    "State Code": "state",
    "Fiscal Year Begin Date": "fiscal_year_start",
    "Fiscal Year End Date": "fiscal_year_end",
    "Net Patient Revenue": "net_patient_revenue",
    "Less Total Operating Expense": "operating_expense",
    "Net Income from Service to Patients": "reported_service_income",
    "Net Income": "net_income",
    "Total Salaries From Worksheet A": "total_salaries",
    "Total Days (V + XVIII + XIX + Unknown)": "patient_days"
}

hospital = df[list(columns)].rename(columns=columns).copy()

# Convert financial fields to numeric values
numeric_columns = [
    "net_patient_revenue",
    "operating_expense",
    "reported_service_income",
    "net_income",
    "total_salaries",
    "patient_days"
]

for col in numeric_columns:
    hospital[col] = pd.to_numeric(
        hospital[col], errors="coerce"
    )

# Calculate patient-service operating income
hospital["calculated_service_income"] = (
    hospital["net_patient_revenue"]
    - hospital["operating_expense"]
)

# Only calculate margins with positive revenue
valid_revenue = hospital["net_patient_revenue"] > 0

hospital["operating_margin_pct"] = (
    hospital["calculated_service_income"]
    / hospital["net_patient_revenue"].where(valid_revenue)
) * 100

# Check calculated income against CMS-reported income
hospital["income_difference"] = (
    hospital["calculated_service_income"]
    - hospital["reported_service_income"]
)

# Save complete modeled dataset
output = processed / "hospital_financial_model.csv"
hospital.to_csv(output, index=False)

print("\nFINANCIAL MODEL CREATED")
print(f"Hospital records: {len(hospital):,}")
print(f"Valid margins: {hospital['operating_margin_pct'].notna().sum():,}")

# Check financial reconciliation
differences = hospital["income_difference"].dropna()
print("\nINCOME RECONCILIATION")
print(f"Records compared: {len(differences):,}")
print(f"Records with difference > $1: {(differences.abs() > 1).sum():,}")

# Preview Kentucky hospitals
kentucky = hospital[
    (hospital["state"] == "KY")
    & hospital["operating_margin_pct"].notna()
]

print("\nKENTUCKY HOSPITALS")
print(f"Records with valid margins: {len(kentucky):,}")

print(
    kentucky[
        [
            "hospital_name",
            "net_patient_revenue",
            "operating_expense",
            "operating_margin_pct"
        ]
    ].head(10).to_string(index=False)
)

print(f"\nSaved to: {output}")
print("\nFinancial model complete!")
