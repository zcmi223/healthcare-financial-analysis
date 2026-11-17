
from pathlib import Path
import pandas as pd

root = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    root / "data/processed/hospital_financial_model.csv",
    dtype={"provider_ccn": "string"}
)

# Convert dates
df["fiscal_year_start"] = pd.to_datetime(
    df["fiscal_year_start"], errors="coerce"
)
df["fiscal_year_end"] = pd.to_datetime(
    df["fiscal_year_end"], errors="coerce"
)

# Calculate reporting period
df["reporting_days"] = (
    df["fiscal_year_end"] - df["fiscal_year_start"]
).dt.days + 1

# Select approximately full-year reports
valid = df[
    df["reporting_days"].between(350, 380)
    & (df["net_patient_revenue"] > 0)
    & df["operating_expense"].notna()
    & df["provider_ccn"].notna()
].copy()

# Find multiple eligible reports for the same provider
duplicates = valid[
    valid.duplicated("provider_ccn", keep=False)
].sort_values(["provider_ccn", "fiscal_year_end"])

duplicates.to_csv(
    root / "data/processed/benchmark_duplicates.csv",
    index=False
)

# Keep only providers with one eligible report
benchmark = valid[
    ~valid.duplicated("provider_ccn", keep=False)
].copy()

# Recalculate operating margin
benchmark["operating_margin_pct"] = (
    (
        benchmark["net_patient_revenue"]
        - benchmark["operating_expense"]
    ) / benchmark["net_patient_revenue"]
) * 100

# Identify Kentucky hospitals
kentucky = benchmark[
    benchmark["state"] == "KY"
].copy()

# Save outputs
processed = root / "data/processed"

benchmark.to_csv(
    processed / "benchmark_hospitals.csv",
    index=False
)

kentucky.to_csv(
    processed / "kentucky_hospitals.csv",
    index=False
)

print("\nBENCHMARK DATA SUMMARY")
print("Original records:", len(df))
print("Eligible full-year records:", len(valid))
print("Records with duplicate eligible CCNs:", len(duplicates))
print("Benchmark records:", len(benchmark))
print("Kentucky benchmark records:", len(kentucky))

print("\nKENTUCKY HOSPITALS")
print(
    kentucky[
        [
            "provider_ccn",
            "hospital_name",
            "fiscal_year_end",
            "operating_margin_pct"
        ]
    ].sort_values("hospital_name").to_string(index=False)
)

print("\nBenchmark preparation complete!")
