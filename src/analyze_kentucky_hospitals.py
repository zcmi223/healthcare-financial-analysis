
from pathlib import Path
import duckdb
import pandas as pd

root = Path(__file__).resolve().parent.parent
file = root / "data/processed/kentucky_hospitals.csv"

df = pd.read_csv(file, dtype={"provider_ccn": "string"})

con = duckdb.connect()
con.register("hospitals", df)

# Compare only reports ending in 2025
query = """
SELECT
    provider_ccn,
    hospital_name,
    fiscal_year_end,
    ROUND(net_patient_revenue / 1000000, 1)
        AS revenue_millions,
    ROUND(operating_expense / 1000000, 1)
        AS expense_millions,
    ROUND(operating_margin_pct, 2)
        AS operating_margin_pct
FROM hospitals
WHERE TRY_CAST(fiscal_year_end AS DATE)
      BETWEEN DATE '2025-01-01' AND DATE '2025-12-31'
  AND net_patient_revenue > 0
ORDER BY net_patient_revenue DESC
"""

results = con.execute(query).df()

print("\n2025 KENTUCKY HOSPITAL FINANCIAL COMPARISON")
print(results.head(20).to_string(index=False))

print("\nNUMBER OF HOSPITALS:", len(results))
print(
    "MEDIAN OPERATING MARGIN:",
    round(results["operating_margin_pct"].median(), 2),
    "%"
)

# Save results
output = root / "data/processed/ky_2025_benchmark.csv"
results.to_csv(output, index=False)

print("\nSaved:", output)
print("SQL analysis complete!")
