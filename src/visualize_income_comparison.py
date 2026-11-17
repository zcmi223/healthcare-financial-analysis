
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    root / "reports/teaching_hospital_income_comparison.csv"
)

# Shorten labels for a readable chart
names = {
    "UNIVERSITY HOSPITAL": "University Hospital (KY)",
    "MEMORIAL HERMANN TEXAS MEDICAL CNTR": "Memorial Hermann",
    "DUKE UNIVERSITY HOSPITAL": "Duke University",
    "UPMC - PRESBYTERIAN SHADYSIDE": "UPMC Presbyterian",
    "THE OHIO STATE UNIVERSITY HOSPITAL": "Ohio State",
    "UF HEALTH SHANDS": "UF Health Shands",
    "OU MEDICAL CENTER": "OU Medical Center",
    "UCSD MEDICAL CENTER": "UCSD Medical Center",
    "CEDARS-SINAI MEDICAL CENTER": "Cedars-Sinai",
    "UNIVERSITY OF CO HOSPITAL": "University of Colorado",
    "VCU HEALTH SYSTEM MCV HOSPITAL": "VCU Health"
}

df["label"] = df["hospital"].replace(names)
df = df.sort_values("service_margin_pct")

fig, ax = plt.subplots(figsize=(12, 8))

y = range(len(df))
height = 0.38

ax.barh(
    [i - height / 2 for i in y],
    df["service_margin_pct"],
    height=height,
    label="Patient-service margin"
)

ax.barh(
    [i + height / 2 for i in y],
    df["net_margin_pct"],
    height=height,
    label="Net-income margin"
)

ax.set_yticks(list(y))
ax.set_yticklabels(df["label"])
ax.axvline(0, color="gray", linewidth=1)

ax.set_xlabel("Margin (%)")
ax.set_title(
    "Teaching Hospitals: Patient-Service vs. Net-Income Margins",
    fontweight="bold"
)

ax.legend()
ax.grid(axis="x", alpha=0.2)

plt.tight_layout()

output = root / "reports" / "teaching_hospital_income_chart.png"
plt.savefig(output, dpi=300, bbox_inches="tight")
plt.show()

print(f"Chart saved to: {output}")
