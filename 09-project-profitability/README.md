# Project Profitability Dashboard

Find unprofitable engagements, budget overruns and differences between project revenue, invoices and receipts.

**Status:** implemented PBIP/PBIR source with synthetic demo data. Windows Power BI Desktop open/refresh, DAX evaluation, rendered appearance and Service deployment have not been executed. Not yet a client-certified release or exported PBIX.

## Open

1. Download/extract the Astra repository to a short Windows path.
2. Open `Dashboard.pbip` in current Power BI Desktop. Enable PBIP/PBIR options if your release requires them, then restart.
3. Click **Refresh**. `DataMode = Demo` uses embedded fixtures and requires no data-file path or account.
4. Review the three report tabs; use the dropdown filters and select chart categories to explore.
5. Run `Model.SemanticModel/DAXQueries/Reconcile.dax` in DAX query view and compare against `validation/expected-demo.json`.

## Report pages

- **Portfolio profitability:** Recognized Revenue, Project Profit, Project Margin, Budget Remaining
- **Delivery and budgets:** Delivery Cost, Cost Budget, Hours Variance, Effective Revenue per Hour
- **Billing and collections:** Invoiced, Collected, Invoice Cash Gap, Recognized Revenue

### Page guidance

- **Portfolio profitability:** Recognized revenue is accrual-based and separate from invoicing and cash collection.
- **Delivery and budgets:** Cost budget is allocated by month. Positive hours variance means actual hours exceeded plan.
- **Billing and collections:** Invoice cash gap is a period comparison, not an overdue receivables balance.

## Business scope

Jan–Sep 2026 monthly project performance.

One row per project/month. Recognized revenue is independent of invoices and cash. CostBudget is allocated monthly, not a repeated full-project budget. Collections can exceed current invoices with opening receivables in real data. Invoice cash gap is not an overdue balance; opening receivables and due dates are outside scope.

## KPI definitions

| Metric | Definition |
|---|---|
| Recognized Revenue | Accrual revenue recognized for the reporting period. |
| Labor Cost | Sum of LaborCost at the recorded grain. |
| Subcontract Cost | Sum of SubcontractCost at the recorded grain. |
| Expenses | Sum of Expenses at the recorded grain. |
| Delivery Cost | Direct project delivery cost excluding general overhead. |
| Project Profit | Recognized revenue less direct delivery cost. |
| Project Margin | Project profit / recognized revenue. |
| Cost Budget | Monthly allocated direct delivery budget. |
| Budget Remaining | Allocated budget less actual cost; positive is under budget. |
| Actual Hours | Sum of ActualHours at the recorded grain. |
| Planned Hours | Sum of PlannedHours at the recorded grain. |
| Hours Variance | Positive means more hours consumed than planned. |
| Effective Revenue per Hour | Recognized revenue per actual delivery hour. |
| Invoiced | Sum of Invoiced at the recorded grain. |
| Collected | Sum of Collected at the recorded grain. |
| Invoice Cash Gap | Selected-period invoices minus collections. Not accounts-receivable balance or overdue debt. |

## Connect customer data

Copy `data/import-template/*.csv` to a private folder and fill every required table using [DATA-CONTRACT.md](DATA-CONTRACT.md). The demo CSVs provide populated examples. In Transform data → Manage parameters set `DataMode` to `Folder` and `DataFolder` to that folder. Keep `Metrics.csv` with its supplied single row. Refresh and reconcile source totals before delivery. Expand Calendar to cover every transaction date and relevant comparison period. Do not commit customer data here.

See [shared setup](../docs/SETUP.md) and [acceptance checklist](../docs/ACCEPTANCE.md). Model relationships, Power Query and DAX are editable source files. The builder overwrites generated artifacts; preserve Desktop edits before rebuilding.
