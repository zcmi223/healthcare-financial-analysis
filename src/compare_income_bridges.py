
from pathlib import Path
import pandas as pd

root = Path(__file__).resolve().parent.parent
processed = root / "data" / "processed"
reports = root / "reports"
reports.mkdir(exist_ok=True)

df = pd.read_csv(
    processed / "national_income_bridge.csv",
    dtype={"ccn": "string"}
)

# Retain University Hospital and its 10 closest peers
target = df[df["ccn"] == "180067"]

if len(target) != 1:
    raise ValueError("University Hospital not uniquely identified")

closest = (
    df[df["ccn"] != "180067"]
    .sort_values("similarity_score")
    .head(10)
)

comparison = pd.concat([target, closest]).copy()

# Reconcile missing financial statement components
comparison["other_income_adjusted"] = (
    comparison["other_income"].fillna(0)
)

comparison["other_expenses_adjusted"] = (
    comparison["other_expenses"].fillna(0)
)

comparison["bridge_difference"] = (
    comparison["service_income"]
    + comparison["other_income_adjusted"]
    - comparison["other_expenses_adjusted"]
    - comparison["net_income"]
)

if comparison["bridge_difference"].abs().gt(1).any():
    raise ValueError("Income bridge reconciliation failed")

# Compare financial results
comparison["margin_improvement_pp"] = (
    comparison["net_margin_pct"]
    - comparison["service_margin_pct"]
)

columns = [
    "hospital",
    "state",
    "service_margin_pct",
    "net_margin_pct",
    "margin_improvement_pp",
    "other_income",
    "net_income"
]

results = comparison[columns].copy()

print("\nNATIONAL TEACHING HOSPITAL INCOME COMPARISON")
print(results.round(2).to_string(index=False))

print("\nCLOSEST 10 PEERS — MEDIAN MARGINS")
print(
    "Service margin:",
    round(closest["service_margin_pct"].median(), 2)
)

print(
    "Net margin:",
    round(closest["net_margin_pct"].median(), 2)
)

output = reports / "teaching_hospital_income_comparison.csv"
results.to_csv(output, index=False)

print("\nSaved:", output)
print("Income comparison complete!")
