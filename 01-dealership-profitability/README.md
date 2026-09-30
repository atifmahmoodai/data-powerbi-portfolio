# Car Dealership Profitability & Inventory

Identify profitable vehicles, compare branches and review capital trapped in ageing stock.

**Status:** implemented PBIP/PBIR source with synthetic demo data. Windows Power BI Desktop open/refresh, DAX evaluation, rendered appearance and Service deployment have not been executed. Not yet a client-certified release or exported PBIX.

## Open

1. Download/extract the Astra repository to a short Windows path.
2. Open `Dashboard.pbip` in current Power BI Desktop. Enable PBIP/PBIR options if your release requires them, then restart.
3. Click **Refresh**. `DataMode = Demo` uses embedded fixtures and requires no data-file path or account.
4. Review the three report tabs; use the dropdown filters and select chart categories to explore.
5. Run `Model.SemanticModel/DAXQueries/Reconcile.dax` in DAX query view and compare against `validation/expected-demo.json`.

## Report pages

- **Executive overview:** Sales Revenue, Gross Profit, Stock Value, Aged Stock Units
- **Stock ageing:** Stock Units, Stock Value, Average Stock Age, Aged Stock Value
- **Sales performance:** Units Sold, Sales Revenue, Gross Margin, Average Days to Sell

## Business scope

Current stock at 30 Sep 2026; completed sales by sale date.

One row per vehicle lifecycle. Sold vehicles require SaleDate >= PurchaseDate and nonzero SalePrice; unsold vehicles have blank SaleDate and zero SalePrice. Stock is a current snapshot, not historical inventory. No leads or conversion rate are inferred.

## KPI definitions

| Metric | Definition |
|---|---|
| Units Sold | Count of vehicles with completed sales. |
| Sales Revenue | Sale price of sold vehicles, excluding tax. |
| Sold Vehicle Cost | Purchase plus reconditioning cost of sold vehicles. |
| Gross Profit | Vehicle gross profit before finance costs and operating overhead. |
| Gross Margin | Vehicle gross profit divided by sales revenue. |
| Stock Units | Vehicles in stock at the 30 September 2026 snapshot. |
| Stock Value | Capitalized purchase and reconditioning cost of current stock. |
| Average Stock Age | Average days since purchase for current stock. |
| Aged Stock Units | Current unsold vehicles older than 90 days. |
| Aged Stock Value | Cost tied up in stock older than 90 days. |
| Average Days to Sell | Mean purchase-to-sale duration of completed sales. |
| Profit per Vehicle | Mean gross profit per sold vehicle. |

## Connect customer data

Copy `data/import-template/*.csv` to a private folder and fill every required table using [DATA-CONTRACT.md](DATA-CONTRACT.md). The demo CSVs provide populated examples. In Transform data → Manage parameters set `DataMode` to `Folder` and `DataFolder` to that folder. Keep `Metrics.csv` with its supplied single row. Refresh and reconcile source totals before delivery. Expand Calendar to cover every transaction date and relevant comparison period. Do not commit customer data here.

See [shared setup](../docs/SETUP.md) and [acceptance checklist](../docs/ACCEPTANCE.md). Model relationships, Power Query and DAX are editable source files. The builder overwrites generated artifacts; preserve Desktop edits before rebuilding.
