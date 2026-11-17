
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    root / "data/processed/ky_large_hospital_peers.csv",
    dtype={"provider_ccn": "string"}
)

# Sort from lowest to highest operating margin
df = df.sort_values("operating_margin_pct")

median_margin = df["operating_margin_pct"].median()

# Highlight University Hospital
colors = [
    "#D97732" if ccn == "180067" else "#4472C4"
    for ccn in df["provider_ccn"]
]

fig, ax = plt.subplots(figsize=(12, 7))

bars = ax.barh(
    df["hospital_name"],
    df["operating_margin_pct"],
    color=colors
)

# Add comparison line
ax.axvline(
    median_margin,
    color="black",
    linestyle="--",
    linewidth=1.5,
    label=f"Peer median: {median_margin:.2f}%"
)

ax.axvline(0, color="gray", linewidth=0.8)

# Label each hospital margin
for bar, margin in zip(bars, df["operating_margin_pct"]):
    ax.annotate(
        f"{margin:+.2f}%",
        xy=(margin, bar.get_y() + bar.get_height() / 2),
        xytext=(5 if margin >= 0 else -5, 0),
        textcoords="offset points",
        ha="left" if margin >= 0 else "right",
        va="center",
        fontsize=9
    )

ax.set_xlim(
    min(-35, df["operating_margin_pct"].min() - 5),
    max(25, df["operating_margin_pct"].max() + 5)
)

ax.set_title(
    "Kentucky Large Hospital Operating Margins\n"
    "Fiscal Years Ending 2025",
    fontsize=15,
    fontweight="bold"
)

ax.set_xlabel("Patient-Service Operating Margin (%)")
ax.legend(loc="lower right")

fig.text(
    0.5, 0.01,
    "Source: CMS hospital cost reports. "
    "Hospitals with $500M+ net patient revenue. "
    "Reporting periods and hospital types may differ.",
    ha="center",
    fontsize=8
)

plt.tight_layout(rect=[0, 0.04, 1, 1])

output = root / "reports" / "kentucky_margin_comparison.png"
output.parent.mkdir(parents=True, exist_ok=True)

plt.savefig(output, dpi=300, bbox_inches="tight")
plt.show()

print(f"\nChart saved to: {output}")
print("Visualization complete!")
