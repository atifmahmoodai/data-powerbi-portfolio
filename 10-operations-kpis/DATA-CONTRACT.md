# Data contract

UTF-8 CSV, comma delimiter, ISO dates, period decimal separator. Preserve exact column names. All amounts are PKR, excluding taxes unless explicitly stated. Do not mix currencies. Blank nullable dates are allowed only where documented. Keys must be unique at the declared grain and foreign keys must resolve.

Month means CreatedDate. CompletedDate is required for Completed and blank for Open. OnTime and Rework are 0/1 and zero for open jobs. CompletedDate >= CreatedDate; CycleDays must match. DueDate is a calendar-date SLA, not business-hour SLA. Update as-of DATE in overdue measure when using a newer snapshot. Historical backlog and completion-date throughput need a separate event history.

## Teams

Grain: one operations team. Unique key: `TeamID`.

| Column | Type |
|---|---|
| TeamID | string |
| Team | string |
| Location | string |

## Jobs

Grain: one current job snapshot. Unique key: `JobID`.

| Column | Type |
|---|---|
| JobID | string |
| TeamID | string |
| Service | string |
| Priority | string |
| CreatedDate | dateTime |
| DueDate | dateTime |
| CompletedDate | dateTime |
| Status | string |
| CycleDays | int64 |
| OnTime | int64 |
| Rework | int64 |
| Cost | decimal |

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