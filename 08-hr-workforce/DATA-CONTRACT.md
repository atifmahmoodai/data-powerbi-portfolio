# Data contract

UTF-8 CSV, comma delimiter, ISO dates, period decimal separator. Preserve exact column names. All amounts are PKR, excluding taxes unless explicitly stated. Do not mix currencies. Blank nullable dates are allowed only where documented. Keys must be unique at the declared grain and foreign keys must resolve.

ClosingHeadcount = OpeningHeadcount + Hires - Leavers. Next month opening equals prior closing. All departments must have the same month coverage. AbsentHours <= ScheduledHours. Aggregate, synthetic HR data only; access controls for real employee information must be designed before deployment.

## Departments

Grain: one department. Unique key: `DepartmentID`.

| Column | Type |
|---|---|
| DepartmentID | string |
| Department | string |
| Location | string |

## Workforce

Grain: one department per month-end. Unique key: `SnapshotID`.

| Column | Type |
|---|---|
| SnapshotID | string |
| DepartmentID | string |
| Date | dateTime |
| OpeningHeadcount | int64 |
| ClosingHeadcount | int64 |
| Hires | int64 |
| Leavers | int64 |
| ScheduledHours | int64 |
| AbsentHours | int64 |
| OvertimeHours | int64 |
| Payroll | decimal |

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