
from pathlib import Path
import pandas as pd

root = Path(__file__).resolve().parent.parent
raw = root / "data" / "raw"
processed = root / "data" / "processed"

# Load the nine hospitals we've been analyzing
peers = pd.read_csv(
    processed / "ky_large_hospital_peers.csv",
    dtype={"provider_ccn": "string"}
)

# Locate the original CMS file
files = list(raw.glob("*.csv"))

if len(files) != 1:
    raise ValueError("Expected exactly one CMS CSV in data/raw")

cms = pd.read_csv(files[0], low_memory=False)

# Identify relevant hospital characteristics
columns = {
    "Provider CCN": "provider_ccn",
    "Hospital Name": "hospital_name",
    "Fiscal Year End Date": "fiscal_year_end",
    "CCN Facility Type": "facility_type",
    "Rural Versus Urban": "rural_urban",
    "Number of Beds": "beds",
    "Number of Interns and Residents (FTE)": "resident_fte",
    "FTE - Employees on Payroll": "employee_fte",
    "Overhead Non-Salary Costs": "overhead_costs",
    "Contract Labor: Direct Patient Care": "contract_labor",
    "Depreciation Cost": "depreciation"
}

cms = cms[list(columns)].rename(columns=columns)

# Standardize identifiers and dates
for df in [peers, cms]:
    df["provider_ccn"] = (
        df["provider_ccn"].astype("string").str.zfill(6)
    )
    df["fiscal_year_end"] = pd.to_datetime(
        df["fiscal_year_end"], errors="coerce"
    )

keys = ["provider_ccn", "fiscal_year_end"]

# Match original CMS records to selected peer hospitals
matched = cms.merge(
    peers[keys],
    on=keys,
    how="inner"
)

# Do not select between ambiguous CMS records
if matched.duplicated(keys).any():
    ambiguous = matched[
        matched.duplicated(keys, keep=False)
    ]
    ambiguous.to_csv(
        processed / "ambiguous_peer_profiles.csv",
        index=False
    )
    raise ValueError(
        "Multiple CMS records match a peer. "
        "Review ambiguous_peer_profiles.csv"
    )

# Merge hospital characteristics into existing peer data
profile = peers.merge(
    matched.drop(columns=["hospital_name"]),
    on=keys,
    how="left",
    validate="one_to_one",
    indicator=True
)

if (profile["_merge"] != "both").any():
    raise ValueError("Some peer hospitals did not match CMS data")

profile = profile.drop(columns="_merge")

# Calculate resident physicians per 100 beds
beds = pd.to_numeric(profile["beds"], errors="coerce")
residents = pd.to_numeric(
    profile["resident_fte"], errors="coerce"
)

profile["residents_per_100_beds"] = (
    residents / beds.where(beds > 0) * 100
)

# Save detailed results
output = processed / "hospital_peer_profiles.csv"
profile.to_csv(output, index=False)

print("\nHOSPITAL PEER CHARACTERISTICS")

display = [
    "hospital_name",
    "facility_type",
    "rural_urban",
    "beds",
    "resident_fte",
    "residents_per_100_beds",
    "operating_margin_pct"
]

print(profile[display].round(2).to_string(index=False))

print("\nMISSING VALUES")
print(profile[display].isna().sum().to_string())

print("\nSaved:", output)
print("Peer profiling complete!")
