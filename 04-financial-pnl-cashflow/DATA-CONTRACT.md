# Data contract

UTF-8 CSV, comma delimiter, ISO dates, period decimal separator. Preserve exact column names. All amounts are PKR, excluding taxes unless explicitly stated. Do not mix currencies. Blank nullable dates are allowed only where documented. Keys must be unique at the declared grain and foreign keys must resolve.

PnL actual and budget amounts are positive; Category determines income/cost sign. CashMovement is signed (receipts positive). P&L and cash must be reconciled independently; there is no inferred bank balance. Monthly dates are month starts. Tax, interest, balance sheet, AR/AP ageing and cash forecasts are excluded.

## Departments

Grain: one department. Unique key: `DepartmentID`.

| Column | Type |
|---|---|
| DepartmentID | string |
| Department | string |

## PnL

Grain: one department/category/month. Unique key: `LineID`.

| Column | Type |
|---|---|
| LineID | string |
| DepartmentID | string |
| Date | dateTime |
| Category | string |
| Actual | decimal |
| Budget | decimal |

## Cash

Grain: one department/cash category/month. Unique key: `CashID`.

| Column | Type |
|---|---|
| CashID | string |
| DepartmentID | string |
| Date | dateTime |
| Category | string |
| CashMovement | decimal |

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