# Data contract

UTF-8 CSV, comma delimiter, ISO dates, period decimal separator. Preserve exact column names. All amounts are PKR, excluding taxes unless explicitly stated. Do not mix currencies. Blank nullable dates are allowed only where documented. Keys must be unique at the declared grain and foreign keys must resolve.

SalesID is unique; Units > 0. Targets have exactly one row per account/date. Revenue is net of discounts, before tax. Customer attributes describe current ownership, not historical salesperson assignment.

## Accounts

Grain: one customer account. Unique key: `AccountID`.

| Column | Type |
|---|---|
| AccountID | string |
| Customer | string |
| Region | string |
| Segment | string |
| Salesperson | string |

## Sales

Grain: one sales transaction. Unique key: `SalesID`.

| Column | Type |
|---|---|
| SalesID | string |
| AccountID | string |
| Date | dateTime |
| Units | int64 |
| Revenue | decimal |
| Cost | decimal |

## Targets

Grain: one account per day. Unique key: `TargetID`.

| Column | Type |
|---|---|
| TargetID | string |
| AccountID | string |
| Date | dateTime |
| TargetRevenue | decimal |

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