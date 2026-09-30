# Data contract

UTF-8 CSV, comma delimiter, ISO dates, period decimal separator. Preserve exact column names. All amounts are PKR, excluding taxes unless explicitly stated. Do not mix currencies. Blank nullable dates are allowed only where documented. Keys must be unique at the declared grain and foreign keys must resolve.

Month means CreatedDate, not ClosedDate. Stage histories and historical pipeline are unavailable. ClosedDate is required for Won/Lost and blank for open stages. Probability lies in [0,1]. Update fixed as-of DATE in stale-deal measures for a new reporting snapshot. No personal customer data is included.

## Owners

Grain: one sales owner. Unique key: `OwnerID`.

| Column | Type |
|---|---|
| OwnerID | string |
| Owner | string |
| Team | string |

## Opportunities

Grain: one current opportunity snapshot. Unique key: `OpportunityID`.

| Column | Type |
|---|---|
| OpportunityID | string |
| OwnerID | string |
| Source | string |
| Stage | string |
| CreatedDate | dateTime |
| ClosedDate | dateTime |
| LastActivityDate | dateTime |
| Amount | decimal |
| Probability | decimal |
| CycleDays | int64 |
| IsOpen | int64 |

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