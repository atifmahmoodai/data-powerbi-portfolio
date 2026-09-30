# Data contract

UTF-8 CSV, comma delimiter, ISO dates, period decimal separator. Preserve exact column names. All amounts are PKR, excluding taxes unless explicitly stated. Do not mix currencies. Blank nullable dates are allowed only where documented. Keys must be unique at the declared grain and foreign keys must resolve.

OrderID is unique. Refund <= GrossSales - Discount. NetCOGS reflects recoverable returns; payment/shipping costs may remain after a refund. AdSpend is one row per channel/date. Revenue-to-spend is blended efficiency, not causal ad attribution. No CAC, LTV or accounting net profit claims.

## Channels

Grain: one acquisition/sales channel. Unique key: `ChannelID`.

| Column | Type |
|---|---|
| ChannelID | string |
| Channel | string |
| Market | string |

## Orders

Grain: one order. Unique key: `OrderID`.

| Column | Type |
|---|---|
| OrderID | string |
| ChannelID | string |
| Date | dateTime |
| CustomerID | string |
| GrossSales | decimal |
| Discount | decimal |
| Refund | decimal |
| NetCOGS | decimal |
| ShippingCost | decimal |
| PaymentFee | decimal |
| FulfilmentCost | decimal |

## Advertising

Grain: one channel per day. Unique key: `SpendID`.

| Column | Type |
|---|---|
| SpendID | string |
| ChannelID | string |
| Date | dateTime |
| AdSpend | decimal |

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