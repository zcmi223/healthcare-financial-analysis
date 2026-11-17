# Hospital Financial Performance & Benchmarking
**Executive Financial Analysis | Fiscal Years Ending 2025**

**Data Source:** Centers for Medicare & Medicaid Services (CMS), Hospital Provider Cost Reports  
**Tools:** Python, DuckDB SQL, Power BI  
**Primary Focus:** University Hospital, Kentucky (Provider CCN 180067)

---

## 1. Executive Summary

An analysis of CMS hospital cost-report data identified substantial differences between hospital patient-service profitability and overall reported net income.

The analysis included 133 large teaching hospitals nationally, a comparison of 10 similarly sized and teaching-intensive hospitals, and a separate group of nine large Kentucky hospitals.

University Hospital reported a **patient-service operating loss of $665.4 million**, representing a −27.04% patient-service margin. However, after accounting for reported other income, the hospital generated **positive net income of $462.1 million**, equivalent to 18.78% of net patient revenue.

This difference demonstrates why evaluating hospital financial performance requires understanding both patient-service operations and non-patient-service financial activity.

## 2. Key Financial Results

| Financial Metric | University Hospital |
|---|---:|
| Net Patient Revenue | $2.461 billion |
| Operating Expenses | $3.126 billion |
| Patient-Service Operating Income | −$665.4 million |
| Patient-Service Operating Margin | −27.04% |
| Reported Other Income | $1.127 billion |
| Overall Net Income | +$462.1 million |
| Net Income / Patient Revenue | +18.78% |

**Finding:** Reported other income more than offset the loss from patient services. The underlying composition and sustainability of this income require further investigation.

## 3. National Teaching-Hospital Benchmarking

The national teaching-hospital group contained 133 hospitals meeting preliminary screening requirements for hospital size, resident physician staffing, reporting period, and available financial data.

| Profitability Metric | University Hospital | National Median |
|---|---:|---:|
| Patient-Service Margin | −27.04% | −2.56% |
| Net-Income Margin | +18.78% | +8.85% |

University Hospital's patient-service margin was approximately 24.49 percentage points below the national median, while its net-income margin was approximately 9.92 percentage points above the national median.

Among the 10 closest hospitals selected by bed count and resident physicians per 100 beds, the median patient-service margin was approximately +0.80%, and the median net-income margin was +6.57%.

These results suggest substantial differences in reported financial structure, but do not establish that University Hospital is operationally less efficient than its peers.

## 4. Expense and Labor Analysis

A separate analysis of nine large Kentucky hospitals identified the following University Hospital results:

| Metric | University Hospital | Kentucky Peer Median |
|---|---:|---:|
| Operating Expenses / Revenue | 127.04% | 102.07% |
| Reported Salaries / Revenue | 35.75% | 25.43% |
| Reported Salaries / Operating Expenses | 28.14% | 27.10% |

University Hospital reported higher salaries relative to revenue, but a salary share of operating expenses only slightly above the Kentucky peer median.

This suggests that the financial performance difference cannot be attributed to reported salary expenses alone.

Further analysis should examine non-salary operating costs, reimbursement, contracted labor, service mix, and cost allocation methods.

## 5. Recommended Management Investigations

**Revenue and reimbursement:** Evaluate patient-service revenue by payer, service line, and utilization category to identify potential differences in reimbursement and revenue mix.

**Labor and staffing:** Examine employee compensation, contracted labor, staffing productivity, and reported resident physician activity. Reconcile reported labor categories before drawing conclusions about labor efficiency.

**Other income:** Determine the composition, timing, restrictions, and recurring nature of other reported income. Assess how sensitive overall reported profitability is to changes in those amounts.

**Peer comparability:** Refine the national comparison using hospital teaching status, case mix, geographic characteristics, service mix, reporting conventions, and organizational structure.

## 6. Data Integrity and Methodology

The analysis used publicly available CMS Hospital Provider Cost Report data. Data preparation included financial reconciliations, reporting-period validation, identification of duplicate provider records, and removal of ambiguous records from initial benchmarks.

National teaching-hospital screening criteria included:

- Fiscal years ending in 2025, with reporting periods of 350–380 days
- At least 300 beds
- At least 100 resident physician FTEs
- Positive reported net patient revenue
- Available operating expense data
- Facility classification of `STH` in the downloaded dataset

The 10 closest national hospitals were identified using a preliminary similarity score based on bed count and resident physician FTE per 100 beds. This is a screening method rather than a statistically validated peer-selection model.

Patient-service operating margin was calculated as:

**(Net Patient Revenue − Operating Expenses) / Net Patient Revenue**

Net-income margin was calculated as:

**Net Income / Net Patient Revenue**

For income bridges, 61 national records had complete components that reconciled within $1. Other-expense values were missing in 72 records; treating these missing amounts as zero produced reconciliations within $1 across all 133 records. This treatment remains a documented assumption requiring confirmation against the source filings.

## 7. Limitations

CMS hospital cost reports do not necessarily represent consolidated health-system financial statements.

Reported financial differences may reflect teaching responsibilities, payer mix, hospital complexity, accounting allocations, reporting conventions, or other factors not fully captured by the analysis.

Salary expense classifications may not include every labor-related cost, and hospital-wide financial amounts divided by inpatient days should not be interpreted as inpatient-only costs or revenues.

The project does not establish causal relationships, management performance, future profitability, or the sustainability of reported other income.

## 8. Conclusion

This analysis demonstrates the importance of separating hospital patient-service operations from overall reported financial performance.

University Hospital's negative patient-service margin and positive net-income margin highlight the need for a more detailed understanding of revenue sources, expense structure, and financial reporting.

The next analytical priority is to examine the composition of other income and develop more closely matched financial comparisons.

The accompanying Power BI dashboard provides interactive financial summaries, income bridges, teaching-hospital benchmarks, and expense-driver comparisons to support further investigation.