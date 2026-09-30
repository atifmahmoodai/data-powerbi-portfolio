# Data contract

UTF-8 CSV, comma delimiter, ISO dates, period decimal separator. Preserve exact column names. All amounts are PKR, excluding taxes unless explicitly stated. Do not mix currencies. Blank nullable dates are allowed only where documented. Keys must be unique at the declared grain and foreign keys must resolve.

0 <= Transactions <= Visitors; Refunds <= GrossSales. NetCOGS must already reflect returned inventory cost. Transaction and visitor counts are events, not distinct people. Targets are one per store/date. No SKU inventory or customer-level identity is implied.

## Stores

Grain: one store. Unique key: `StoreID`.

| Column | Type |
|---|---|
| StoreID | string |
| Store | string |
| Region | string |
| Format | string |

## Trading

Grain: one store per trading date. Unique key: `StoreDayID`.

| Column | Type |
|---|---|
| StoreDayID | string |
| StoreID | string |
| Date | dateTime |
| Visitors | int64 |
| Transactions | int64 |
| Units | int64 |
| GrossSales | decimal |
| Refunds | decimal |
| NetCOGS | decimal |
| Target | decimal |

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