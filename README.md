# Healthcare Financial Performance & Benchmarking

### Python | DuckDB SQL | Power BI | Financial Planning & Analysis

## Project Overview

This project analyzes publicly available CMS hospital cost-report data to evaluate hospital financial performance, compare large teaching hospitals, and investigate differences between patient-service operating profitability and reported net income.

The analysis focuses on University Hospital in Kentucky (Provider CCN 180067) and compares its financial metrics with a national group of teaching hospitals and a separate group of large Kentucky hospitals.

The project demonstrates financial modeling, data validation, SQL analysis, benchmarking, financial visualization, and executive reporting.

## Key Findings

**Patient-service profitability:** University Hospital reported approximately $2.46 billion in net patient revenue and $3.13 billion in operating expenses for its fiscal year ending June 30, 2025, resulting in a patient-service operating margin of −27.04%.

**Overall profitability:** Despite its patient-service operating loss, the hospital reported approximately $462 million in positive net income after other reported income.

**National comparison:** University Hospital's patient-service operating margin was substantially below the −2.56% median of 133 selected national teaching hospitals.

**Expense analysis:** Reported salaries represented approximately 35.75% of net patient revenue, compared with 25.43% for the nine-hospital Kentucky comparison group's median.

These findings identify areas for further investigation rather than establishing causes of financial performance differences.

## Interactive Power BI Dashboard

The Power BI report includes four pages:

1. **Financial Overview:** Revenue, patient-service margins, net-income margins, and hospital selection.
2. **Income Bridge:** Reconciliation of patient-service income, other income, other expenses, and reported net income.
3. **Peer Benchmarking:** Teaching intensity, hospital size, profitability, and national comparisons.
4. **Financial Drivers:** Salary-to-revenue ratios, expense ratios, and patient-service operating income.

The Power BI report file is located in the `dashboard` folder.

## Technical Approach

**Python and pandas:** Data ingestion, standardization, financial calculations, missing-value analysis, and reporting-period validation.

**DuckDB SQL:** Hospital financial comparisons, operating-margin analysis, and benchmarking queries.

**Power BI and DAX:** Interactive dashboards, financial KPI measures, hospital filtering, and comparative visualizations.

**Data quality controls:** Income reconciliations, duplicate-provider checks, source matching, and reporting-period screening.

## Data Source

Centers for Medicare & Medicaid Services (CMS)

[Hospital Provider Cost Report Dataset](https://data.cms.gov/provider-compliance/cost-reports/hospital-provider-cost-report)

The analysis uses the downloaded hospital cost-report dataset and selects reports with fiscal years ending in 2025 where appropriate.

Raw CMS downloads are excluded from this repository and must be obtained from the official source.

## Reproducing the Analysis

1. Install Python and create a virtual environment.
2. Install the dependencies listed in `requirements.txt`.
3. Download the relevant CMS Hospital Provider Cost Report CSV.
4. Extract the CSV into `data/raw`.
5. Run the scripts in `src` in the order documented in the project workflow.
6. Open the Power BI report and configure the local dataset source if necessary.

Some outputs and Power BI connections depend on the locally generated processed CSV files.

## Methodology and Limitations

The national comparison group uses preliminary teaching-hospital screening criteria, including hospital bed count, resident physician staffing, facility classification, fiscal-year reporting period, and availability of financial data.

These criteria are intended for exploratory benchmarking and do not constitute a validated risk-adjusted peer model.

CMS hospital reporting entities do not necessarily represent consolidated healthcare systems. Financial differences may reflect service mix, reimbursement structures, accounting allocations, teaching responsibilities, and reporting conventions.

Missing financial-statement components are not assumed to be zero without reconciliation checks. The composition and recurring nature of other income have not been independently established.

The project is an independent analytical exercise using public data and is not affiliated with CMS or the hospitals analyzed.

## Executive Summary

See `reports/executive_summary.md` for the detailed analysis, key findings, methodology, and recommended management investigations.