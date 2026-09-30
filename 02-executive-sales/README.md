# Executive Sales Performance Dashboard

Compare actual sales against targets, understand margins and evaluate customers and salespeople.

**Status:** implemented PBIP/PBIR source with synthetic demo data. Windows Power BI Desktop open/refresh, DAX evaluation, rendered appearance and Service deployment have not been executed. Not yet a client-certified release or exported PBIX.

## Open

1. Download/extract the Astra repository to a short Windows path.
2. Open `Dashboard.pbip` in current Power BI Desktop. Enable PBIP/PBIR options if your release requires them, then restart.
3. Click **Refresh**. `DataMode = Demo` uses embedded fixtures and requires no data-file path or account.
4. Review the three report tabs; use the dropdown filters and select chart categories to explore.
5. Run `Model.SemanticModel/DAXQueries/Reconcile.dax` in DAX query view and compare against `validation/expected-demo.json`.

## Report pages

- **Revenue and targets:** Revenue, Gross Profit, Target Attainment, Target Variance
- **Customers and margins:** Active Customers, Sales Transactions, Average Transaction, Gross Margin
- **Sales team performance:** Units Sold, Revenue, Gross Profit, Target Attainment

## Business scope

01 Oct 2025–30 Sep 2026 transactions; daily account targets.

SalesID is unique; Units > 0. Targets have exactly one row per account/date. Revenue is net of discounts, before tax. Customer attributes describe current ownership, not historical salesperson assignment.

## KPI definitions

| Metric | Definition |
|---|---|
| Revenue | Sum of Revenue at the recorded grain. |
| Cost of Sales | Sum of Cost at the recorded grain. |
| Gross Profit | Revenue less cost of sales. |
| Gross Margin | Gross profit / revenue. |
| Units Sold | Sum of Units at the recorded grain. |
| Revenue Target | Daily account targets; date and account filters affect actual and target. |
| Target Attainment | Revenue divided by target. |
| Target Variance | Positive means ahead of target. |
| Sales Transactions | Number of sales transactions. |
| Active Customers | Customers with a sale in the selected period. |
| Average Transaction | Revenue per sales transaction. |
| Revenue YTD | Calendar-year revenue through the last selected date; select a populated period. |
| Previous Month Revenue | Revenue in the date selection shifted back one month. Use a single month for month-over-month comparison. |
| Month Growth | Revenue growth versus selected dates shifted back one month; blank if prior revenue is absent. |

## Connect customer data

Copy `data/import-template/*.csv` to a private folder and fill every required table using [DATA-CONTRACT.md](DATA-CONTRACT.md). The demo CSVs provide populated examples. In Transform data → Manage parameters set `DataMode` to `Folder` and `DataFolder` to that folder. Keep `Metrics.csv` with its supplied single row. Refresh and reconcile source totals before delivery. Expand Calendar to cover every transaction date and relevant comparison period. Do not commit customer data here.

See [shared setup](../docs/SETUP.md) and [acceptance checklist](../docs/ACCEPTANCE.md). Model relationships, Power Query and DAX are editable source files. The builder overwrites generated artifacts; preserve Desktop edits before rebuilding.
