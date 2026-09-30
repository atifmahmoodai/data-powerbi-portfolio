# Data contract

UTF-8 CSV, comma delimiter, ISO dates, period decimal separator. Preserve exact column names. All amounts are PKR, excluding taxes unless explicitly stated. Do not mix currencies. Blank nullable dates are allowed only where documented. Keys must be unique at the declared grain and foreign keys must resolve.

One row per project/month. Recognized revenue is independent of invoices and cash. CostBudget is allocated monthly, not a repeated full-project budget. Collections can exceed current invoices with opening receivables in real data. Invoice cash gap is not an overdue balance; opening receivables and due dates are outside scope.

## Projects

Grain: one project. Unique key: `ProjectID`.

| Column | Type |
|---|---|
| ProjectID | string |
| Project | string |
| Client | string |
| Manager | string |
| Service | string |

## Performance

Grain: one project per month. Unique key: `PeriodID`.

| Column | Type |
|---|---|
| PeriodID | string |
| ProjectID | string |
| Date | dateTime |
| RecognizedRevenue | decimal |
| LaborCost | decimal |
| SubcontractCost | decimal |
| Expenses | decimal |
| ActualHours | int64 |
| PlannedHours | int64 |
| CostBudget | decimal |
| Invoiced | decimal |
| Collected | decimal |

## Metrics

Grain: one metadata row. Unique key: `Label`.

| Column | Type |
|---|---|
| Label | string |

## Calendar

Grain: one calendar date. Unique key: `Date`.

| Column | Type |
|---|---|
| Date | dateTime |
| Year | int64 |
| Month | string |
| Quarter | string |