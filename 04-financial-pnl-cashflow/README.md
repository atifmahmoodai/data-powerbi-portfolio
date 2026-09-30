# Financial P&L / Cash Flow Dashboard

Explain operating profit, budget variance and the difference between earned revenue and cash movement.

**Status:** implemented PBIP/PBIR source with synthetic demo data. Windows Power BI Desktop open/refresh, DAX evaluation, rendered appearance and Service deployment have not been executed. Not yet a client-certified release or exported PBIX.

## Open

1. Download/extract the Astra repository to a short Windows path.
2. Open `Dashboard.pbip` in current Power BI Desktop. Enable PBIP/PBIR options if your release requires them, then restart.
3. Click **Refresh**. `DataMode = Demo` uses embedded fixtures and requires no data-file path or account.
4. Review the three report tabs; use the dropdown filters and select chart categories to explore.
5. Run `Model.SemanticModel/DAXQueries/Reconcile.dax` in DAX query view and compare against `validation/expected-demo.json`.

## Report pages

- **Profit and loss:** Revenue, Gross Profit, Operating Profit, Operating Margin
- **Budget performance:** Operating Profit, Budget Profit, Profit Variance, Operating Expense
- **Cash movements:** Cash Inflow, Cash Outflow, Net Cash Movement, Operating Cash Movement

### Page guidance

- **Profit and loss:** Accrual profit is shown here. Customer receipts and payments are reported separately on the Cash movements page.
- **Budget performance:** Positive profit variance means actual operating profit is above budget.
- **Cash movements:** Cash movements only. Opening/closing balances and bank reconciliation are outside this release.

## Business scope

Jan–Sep 2026 monthly accrual P&L and separate cash records.

PnL actual and budget amounts are positive; Category determines income/cost sign. CashMovement is signed (receipts positive). P&L and cash must be reconciled independently; there is no inferred bank balance. Monthly dates are month starts. Tax, interest, balance sheet, AR/AP ageing and cash forecasts are excluded.

## KPI definitions

| Metric | Definition |
|---|---|
| Revenue | Accrual revenue; not customer receipts. |
| Cost of Sales | Positive cost of goods sold. |
| Operating Expense | Positive operating expense excluding COGS. |
| Gross Profit | Revenue less COGS. |
| Operating Profit | Before interest, tax and exceptional items. |
| Operating Margin | Operating profit / accrual revenue. |
| Budget Profit | Budget revenue less budget costs. |
| Profit Variance | Positive means operating profit ahead of budget. |
| Signed Actual | Category-level signed P&L contribution. |
| Signed Budget | Category-level signed budget contribution. |
| Cash Inflow | All positive cash movements including financing. |
| Cash Outflow | Absolute value of all negative cash movements. |
| Net Cash Movement | Cash receipts less payments; not a cash balance. |
| Operating Cash Movement | Receipts less supplier payments and payroll; excludes capex and loans. |

## Connect customer data

Copy `data/import-template/*.csv` to a private folder and fill every required table using [DATA-CONTRACT.md](DATA-CONTRACT.md). The demo CSVs provide populated examples. In Transform data → Manage parameters set `DataMode` to `Folder` and `DataFolder` to that folder. Keep `Metrics.csv` with its supplied single row. Refresh and reconcile source totals before delivery. Expand Calendar to cover every transaction date and relevant comparison period. Do not commit customer data here.

See [shared setup](../docs/SETUP.md) and [acceptance checklist](../docs/ACCEPTANCE.md). Model relationships, Power Query and DAX are editable source files. The builder overwrites generated artifacts; preserve Desktop edits before rebuilding.
