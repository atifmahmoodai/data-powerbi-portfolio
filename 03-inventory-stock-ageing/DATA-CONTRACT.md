# Data contract

UTF-8 CSV, comma delimiter, ISO dates, period decimal separator. Preserve exact column names. All amounts are PKR, excluding taxes unless explicitly stated. Do not mix currencies. Blank nullable dates are allowed only where documented. Keys must be unique at the declared grain and foreign keys must resolve.

Do not sum multiple snapshots. LotID is unique; 0 <= Reserved <= OnHand; UnitCost >= 0; ReceiptDate <= SnapshotDate; AgeDays must match date difference. Ageing is not a demand or reorder calculation.

## Products

Grain: one product. Unique key: `ProductID`.

| Column | Type |
|---|---|
| ProductID | string |
| Product | string |
| Category | string |
| Supplier | string |

## Stock

Grain: one receipt lot in one warehouse. Unique key: `LotID`.

| Column | Type |
|---|---|
| LotID | string |
| ProductID | string |
| Warehouse | string |
| SnapshotDate | dateTime |
| ReceiptDate | dateTime |
| AgeDays | int64 |
| AgeBand | string |
| OnHand | int64 |
| Reserved | int64 |
| UnitCost | decimal |

## Metrics

Grain: one metadata row. Unique key: `Label`.

| Column | Type |
|---|---|
| Label | string |