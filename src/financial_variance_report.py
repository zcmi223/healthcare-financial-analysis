
from pathlib import Path
import duckdb
import pandas as pd

root = Path(__file__).resolve().parent.parent
source = root / "data/processed/financial_driver_analysis.csv"

df = pd.read_csv(source, dtype={"provider_ccn": "string"})

con = duckdb.connect()
con.register("hospitals", df)

query = """
WITH benchmark AS (
    SELECT
        MEDIAN(operating_margin_pct) AS median_margin,
        MEDIAN(salary_to_revenue_pct) AS median_salary_ratio,
        MEDIAN(salary_to_expense_pct) AS median_salary_share
    FROM hospitals
)
SELECT
    h.hospital_name,
    ROUND(h.operating_margin_pct, 2) AS margin_pct,
    ROUND(b.median_margin, 2) AS peer_median_pct,
    ROUND(h.operating_margin_pct - b.median_margin, 2)
        AS margin_gap_pp,
    ROUND(h.salary_to_revenue_pct, 2) AS salary_revenue_pct,
    ROUND(h.salary_to_expense_pct, 2) AS salary_expense_pct,
    ROUND(b.median_salary_ratio, 2) AS peer_salary_revenue_pct,
    ROUND(b.median_salary_share, 2) AS peer_salary_expense_pct
FROM hospitals h
CROSS JOIN benchmark b
ORDER BY margin_gap_pp ASC
"""

results = con.execute(query).df()

print("\nFINANCIAL VARIANCE REPORT")
print(results.to_string(index=False))

university = results[
    df["provider_ccn"] == "180067"
]

print("\nUNIVERSITY HOSPITAL SUMMARY")
print(university.to_string(index=False))

output = root / "reports" / "financial_variance_report.csv"
output.parent.mkdir(parents=True, exist_ok=True)

results.to_csv(output, index=False)

print("\nSaved:", output)
print("Financial variance report complete!")
