# Desktop acceptance — required before client delivery

Status for all ten projects: **pending Windows execution**. Automated source checks are useful evidence, not proof that Power BI has run the queries or rendered the reports.

For each project record Desktop version, tester, date, evidence screenshots and pass/fail:

1. Open `Dashboard.pbip` with no model/report compatibility or repair errors.
2. Refresh in Demo mode. Every query should load without errors. Check row counts against `validation/results.json` and the CSV examples.
3. Run `Model.SemanticModel/DAXQueries/Reconcile.dax` in DAX query view. Compare every metric with `validation/expected-demo.json`; tolerate at most PKR 0.01 for amounts and 0.000001 for ratios.
4. Inspect all three pages at Fit to page. Verify no blank/error visuals, readable labels, sensible axis order, no clipped titles and correct currency/percentage formats.
5. Test each slicer individually and in combination. Clear selections and restore expected totals. Click a chart category and confirm cross-filtering behaves as intended.
6. Test at least one filtered result independently from CSV (one branch, account, store, department, owner, channel, project or team). Grand-total agreement alone does not prove filter correctness.
7. Check the domain-specific cases below.
8. Save, close and reopen. Confirm report integrity. Save As PBIX if the customer requires that format.
9. For customer data, reconcile against its source system and review private sharing, refresh credentials, security requirements and refresh failure monitoring.

| Project | Critical acceptance case |
|---|---|
| Dealership | Stock values exclude sold vehicles; sale-month filters affect completed sales, with stock pages showing the current snapshot |
| Executive sales | Account and month filters affect both actual sales and targets without target duplication |
| Inventory | Lot-age bands reconcile to total stock; reservations never exceed on-hand quantity |
| Finance | Costs subtract from profit; cash is separately sourced; category table uses Signed Actual/Signed Budget |
| Retail | Store conversion is ratio of sums, not average of row percentages |
| E-commerce | Ad spend totals do not multiply with number of orders; refund costs follow the stated policy |
| CRM | Win rate excludes open deals; monthly views represent creation cohorts |
| HR | Nine months of headcount are not summed; attrition uses monthly average opening headcount |
| Projects | Monthly budgets are allocated once; cash gap is not mislabeled overdue receivables |
| Operations | On-time rate denominator includes completed jobs only; month is creation month |

If any acceptance test fails, update the source specification/builder or preserve the corrected Desktop sources before rebuilding. Commit fixes with the failing scenario documented. Do not mark a project production-ready until all applicable tests pass.
