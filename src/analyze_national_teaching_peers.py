
from pathlib import Path
import pandas as pd

root = Path(__file__).resolve().parent.parent
raw = root / "data" / "raw"
processed = root / "data" / "processed"

# Load original CMS data
files = list(raw.glob("*.csv"))
if len(files) != 1:
    raise ValueError("Expected one CSV in data/raw")

df = pd.read_csv(
    files[0],
    low_memory=False,
    dtype={"Provider CCN": "string"}
)

# Select fields needed for national comparison
columns = {
    "Provider CCN": "ccn",
    "Hospital Name": "hospital",
    "State Code": "state",
    "Fiscal Year Begin Date": "start",
    "Fiscal Year End Date": "end",
    "CCN Facility Type": "facility_type",
    "Number of Beds": "beds",
    "Number of Interns and Residents (FTE)": "residents",
    "Net Patient Revenue": "revenue",
    "Less Total Operating Expense": "expenses"
}

df = df[list(columns)].rename(columns=columns)

# Standardize data
df["ccn"] = df["ccn"].str.zfill(6)

for col in ["start", "end"]:
    df[col] = pd.to_datetime(df[col], errors="coerce")

for col in ["beds", "residents", "revenue", "expenses"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["reporting_days"] = (
    df["end"] - df["start"]
).dt.days + 1

# Initial national teaching-hospital filter
peers = df[
    df["end"].dt.year.eq(2025)
    & df["reporting_days"].between(350, 380)
    & (df["beds"] >= 300)
    & (df["residents"] >= 100)
    & (df["revenue"] > 0)
    & df["expenses"].notna()
    & df["ccn"].notna()
    & df["facility_type"].eq("STH")
].copy()

# Exclude ambiguous duplicate providers for review
duplicates = peers[
    peers.duplicated("ccn", keep=False)
].copy()

duplicates.to_csv(
    processed / "national_peer_duplicates.csv",
    index=False
)

peers = peers[
    ~peers.duplicated("ccn", keep=False)
].copy()

# Financial ratios
peers["margin_pct"] = (
    (peers["revenue"] - peers["expenses"])
    / peers["revenue"] * 100
)

peers["residents_per_100_beds"] = (
    peers["residents"] / peers["beds"] * 100
)

peers["revenue_millions"] = peers["revenue"] / 1e6
peers["expense_millions"] = peers["expenses"] / 1e6

# Identify University Hospital
target = peers[peers["ccn"] == "180067"]

if len(target) != 1:
    raise ValueError(
        "University Hospital was not uniquely identified. "
        "Review filtered records before continuing."
    )

university = target.iloc[0]

# Compare hospital size and teaching intensity
# This is a screening score, not a statistical peer model.
peers["similarity_score"] = (
    abs(peers["beds"] - university["beds"])
    / university["beds"]
    + abs(
        peers["residents_per_100_beds"]
        - university["residents_per_100_beds"]
    ) / university["residents_per_100_beds"]
)

# Exclude target when identifying closest alternatives
closest = (
    peers[peers["ccn"] != "180067"]
    .sort_values("similarity_score")
    .head(10)
)

# Save results
peers.to_csv(
    processed / "national_teaching_hospitals.csv",
    index=False
)

closest.to_csv(
    processed / "closest_teaching_peers.csv",
    index=False
)

print("\nNATIONAL TEACHING HOSPITAL COMPARISON")
print("Eligible hospitals:", len(peers))
print("Ambiguous duplicate records:", len(duplicates))
print("National peer median margin:",
      round(peers["margin_pct"].median(), 2), "%")

print("\nUNIVERSITY HOSPITAL")
print(university[
    ["hospital", "beds", "residents", "margin_pct"]
].to_string())

print("\nTEN CLOSEST HOSPITALS BY SIZE AND TEACHING INTENSITY")
print(
    closest[
        [
            "hospital",
            "state",
            "beds",
            "residents_per_100_beds",
            "margin_pct"
        ]
    ].round(2).to_string(index=False)
)

print("\nNational peer analysis complete!")
