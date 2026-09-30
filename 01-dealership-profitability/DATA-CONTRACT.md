# Data contract

UTF-8 CSV, comma delimiter, ISO dates, period decimal separator. Preserve exact column names. All amounts are PKR, excluding taxes unless explicitly stated. Do not mix currencies. Blank nullable dates are allowed only where documented. Keys must be unique at the declared grain and foreign keys must resolve.

One row per vehicle lifecycle. Sold vehicles require SaleDate >= PurchaseDate and nonzero SalePrice; unsold vehicles have blank SaleDate and zero SalePrice. Stock is a current snapshot, not historical inventory. No leads or conversion rate are inferred.

## Vehicles

Grain: one vehicle lifecycle. Unique key: `VehicleID`.

| Column | Type |
|---|---|
| VehicleID | string |
| Make | string |
| Model | string |
| Branch | string |
| Salesperson | string |
| Status | string |
| PurchaseDate | dateTime |
| SaleDate | dateTime |
| PurchaseCost | decimal |
| Reconditioning | decimal |
| SalePrice | decimal |
| DaysHeld | int64 |
| AgeBand | string |

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