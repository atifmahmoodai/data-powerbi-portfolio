# E-commerce Profitability Dashboard

Expose channel contribution after discounts, refunds, fulfilment and advertising costs.

**Status:** implemented PBIP/PBIR source with synthetic demo data. Windows Power BI Desktop open/refresh, DAX evaluation, rendered appearance and Service deployment have not been executed. Not yet a client-certified release or exported PBIX.

## Open

1. Download/extract the Astra repository to a short Windows path.
2. Open `Dashboard.pbip` in current Power BI Desktop. Enable PBIP/PBIR options if your release requires them, then restart.
3. Click **Refresh**. `DataMode = Demo` uses embedded fixtures and requires no data-file path or account.
4. Review the three report tabs; use the dropdown filters and select chart categories to explore.
5. Run `Model.SemanticModel/DAXQueries/Reconcile.dax` in DAX query view and compare against `validation/expected-demo.json`.

## Report pages

- **Profitability overview:** Net Revenue, Contribution after Ads, Contribution Margin, Net AOV
- **Marketing economics:** Ad Spend, Revenue to Ad Spend, Contribution before Ads, Contribution after Ads
- **Discounts and returns:** Gross Sales, Discounts, Refunds, Refund Rate

## Business scope

180-day order cohorts through 30 Sep 2026; refunds attributed to original order date.

OrderID is unique. Refund <= GrossSales - Discount. NetCOGS reflects recoverable returns; payment/shipping costs may remain after a refund. AdSpend is one row per channel/date. Revenue-to-spend is blended efficiency, not causal ad attribution. No CAC, LTV or accounting net profit claims.

## KPI definitions

| Metric | Definition |
|---|---|
| Gross Sales | Sum of GrossSales at the recorded grain. |
| Discounts | Sum of Discount at the recorded grain. |
| Refunds | Sum of Refund at the recorded grain. |
| Net Revenue | Revenue after discounts and refunds, before tax. |
| Net COGS | Cost after recoverable returned goods are restored. |
| Variable Costs | Shipping, payment and fulfilment expenses including nonrefundable return costs. |
| Contribution before Ads | Contribution after order-level costs, before marketing. |
| Ad Spend | Daily channel spend, stored separately to avoid order duplication. |
| Contribution after Ads | Contribution after paid media; not accounting net profit. |
| Contribution Margin | Post-ad contribution / net revenue. |
| Order Count | All placed orders in the supplied cohort, including refunded orders. |
| Net AOV | Net revenue / all cohort orders. |
| Revenue to Ad Spend | Blended net revenue / all paid media spend; not attributed ROAS. |
| Refund Rate | Refund amount / discounted sales. |

## Connect customer data

Copy `data/import-template/*.csv` to a private folder and fill every required table using [DATA-CONTRACT.md](DATA-CONTRACT.md). The demo CSVs provide populated examples. In Transform data → Manage parameters set `DataMode` to `Folder` and `DataFolder` to that folder. Keep `Metrics.csv` with its supplied single row. Refresh and reconcile source totals before delivery. Expand Calendar to cover every transaction date and relevant comparison period. Do not commit customer data here.

See [shared setup](../docs/SETUP.md) and [acceptance checklist](../docs/ACCEPTANCE.md). Model relationships, Power Query and DAX are editable source files. The builder overwrites generated artifacts; preserve Desktop edits before rebuilding.
