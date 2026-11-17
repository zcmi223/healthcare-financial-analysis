
import pandas as pd
import duckdb

# Fictional hospital financial data for testing
hospitals = pd.DataFrame({
    "hospital": ["Hospital A", "Hospital B", "Hospital C"],
    "revenue": [10_000_000, 15_000_000, 12_000_000],
    "expenses": [9_000_000, 13_000_000, 11_500_000]
})

# Calculate operating income and operating margin
hospitals["operating_income"] = (
    hospitals["revenue"] - hospitals["expenses"]
)

hospitals["operating_margin"] = (
    hospitals["operating_income"] / hospitals["revenue"]
)

# Query the financial data using SQL
result = duckdb.sql("""
    SELECT
        hospital,
        revenue,
        expenses,
        operating_income,
        ROUND(operating_margin * 100, 2) AS margin_pct
    FROM hospitals
    ORDER BY margin_pct DESC
""")

print(result.df())
print("\nEnvironment test successful!")
