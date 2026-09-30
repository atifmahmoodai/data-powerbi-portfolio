# Retail Store Performance Dashboard

Compare stores on sales, footfall conversion, basket value, refunds and gross margins.

**Status:** implemented PBIP/PBIR source with synthetic demo data. Windows Power BI Desktop open/refresh, DAX evaluation, rendered appearance and Service deployment have not been executed. Not yet a client-certified release or exported PBIX.

## Open

1. Download/extract the Astra repository to a short Windows path.
2. Open `Dashboard.pbip` in current Power BI Desktop. Enable PBIP/PBIR options if your release requires them, then restart.
3. Click **Refresh**. `DataMode = Demo` uses embedded fixtures and requires no data-file path or account.
4. Review the three report tabs; use the dropdown filters and select chart categories to explore.
5. Run `Model.SemanticModel/DAXQueries/Reconcile.dax` in DAX query view and compare against `validation/expected-demo.json`.

## Report pages

- **Store performance:** Net Sales, Gross Profit, Target Attainment, Store Conversion
- **Footfall and baskets:** Visitors, Transactions, Average Basket, Units Sold
- **Margin and refunds:** Gross Sales, Refunds, Refund Rate, Gross Margin

### Page guidance

- **Footfall and baskets:** Conversion is purchase transactions divided by counted visits, not unique customers. Average basket is net sales per transaction.
- **Margin and refunds:** Net cost of sales already reflects the cost restored for returned inventory.

## Business scope

180 trading days through 30 Sep 2026; one daily record per store.

0 <= Transactions <= Visitors; Refunds <= GrossSales. NetCOGS must already reflect returned inventory cost. Transaction and visitor counts are events, not distinct people. Targets are one per store/date. No SKU inventory or customer-level identity is implied.

## KPI definitions

| Metric | Definition |
|---|---|
| Gross Sales | Sum of GrossSales at the recorded grain. |
| Refunds | Sum of Refunds at the recorded grain. |
| Net Sales | Gross sales less refund amounts, excluding tax. |
| Net Cost of Sales | Cost of sold goods less inventory cost restored by returns. |
| Gross Profit | Net sales less net COGS. |
| Gross Margin | Gross profit / net sales. |
| Visitors | Sum of Visitors at the recorded grain. |
| Transactions | Sum of Transactions at the recorded grain. |
| Units Sold | Gross units sold; return quantities are not supplied. |
| Store Conversion | Purchase transactions / counted store visits; not unique customer conversion. |
| Average Basket | Net sales / purchase transactions. |
| Sales Target | Daily store net sales target. |
| Target Attainment | Net sales / target. |
| Refund Rate | Refund amount / gross sales. |

## Connect customer data

Copy `data/import-template/*.csv` to a private folder and fill every required table using [DATA-CONTRACT.md](DATA-CONTRACT.md). The demo CSVs provide populated examples. In Transform data → Manage parameters set `DataMode` to `Folder` and `DataFolder` to that folder. Keep `Metrics.csv` with its supplied single row. Refresh and reconcile source totals before delivery. Expand Calendar to cover every transaction date and relevant comparison period. Do not commit customer data here.

See [shared setup](../docs/SETUP.md) and [acceptance checklist](../docs/ACCEPTANCE.md). Model relationships, Power Query and DAX are editable source files. The builder overwrites generated artifacts; preserve Desktop edits before rebuilding.
