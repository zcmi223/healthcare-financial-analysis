
from pathlib import Path
import pandas as pd

root = Path(__file__).resolve().parent.parent
file = root / "data/processed/ky_2025_benchmark.csv"

df = pd.read_csv(file, dtype={"provider_ccn": "string"})

# Preliminary peer group: hospitals with $500M+ revenue
peers = df[df["revenue_millions"] >= 500].copy()

# Flag extreme margins for investigation
peers["extreme_margin_flag"] = (
    peers["operating_margin_pct"].abs() > 50
)

# Compare each hospital with the peer median
peer_median = peers["operating_margin_pct"].median()

peers["margin_gap_vs_median_pp"] = (
    peers["operating_margin_pct"] - peer_median
)

# Calculate the expense-to-revenue ratio
peers["expense_ratio_pct"] = (
    peers["expense_millions"]
    / peers["revenue_millions"]
) * 100

# Sort by revenue
peers = peers.sort_values(
    "revenue_millions", ascending=False
)

print("\nLARGE KENTUCKY HOSPITAL COMPARISON")
print(f"Number of hospitals: {len(peers)}")
print(f"Peer median margin: {peer_median:.2f}%")

print(
    peers[
        [
            "hospital_name",
            "revenue_millions",
            "operating_margin_pct",
            "expense_ratio_pct",
            "margin_gap_vs_median_pp",
            "extreme_margin_flag"
        ]
    ].to_string(index=False)
)

output = root / "data/processed/ky_large_hospital_peers.csv"
peers.to_csv(output, index=False)

print("\nSaved:", output)
print("Peer analysis complete!")
