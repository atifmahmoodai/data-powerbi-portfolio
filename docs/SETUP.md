# Setup and customer handover

## Windows demo

Use standard Microsoft Power BI Desktop for Windows. The Report Server edition is not the target. Open the PBIP file together with its adjacent Report and SemanticModel folders; do not move the PBIP alone. PBIP/PBIR options may need to be enabled depending on the installed Desktop release. Restart after changing preview options.

Select Refresh. `DataMode = Demo` reads embedded CSV fixtures. No Python installation, external account, database or gateway is needed for this local demo. Tables can be inspected in Transform data, Model view and Data view. Display formatting uses PKR; changing only the currency label does not convert currency.

## Customer data

1. Agree the business definitions in the project's README, especially stock snapshot dates, revenue recognition, refund treatment, cohort dates and headcount rules.
2. Copy `data/import-template` into a private local folder. Populate all CSVs using the project's DATA-CONTRACT and demo examples. Preserve `Metrics.csv` with the supplied row. No file in this private folder belongs in the public repository.
3. Ensure unique primary keys, valid foreign keys and complete date coverage. Use UTF-8 CSV, ISO dates and period decimal separators. Empty nullable close/sale dates remain empty. Do not put currency symbols in numeric cells.
4. Change `DataMode` to `Folder`, then set `DataFolder` to the private folder through Transform data → Manage parameters. Use an absolute path such as `C:/CustomerData/Analytics`. Power Query errors intentionally surface missing columns and invalid types.
5. Maintain the Calendar table across every source date and required comparison period. The demo contains 2025–2026 calendar dates; it is not an automatically expanding calendar.
6. For dealership/inventory, supply one coherent stock snapshot. For CRM/operations, update the explicit as-of date in stale/overdue DAX measures when updating the snapshot. Their README describes the date basis.
7. Refresh, reconcile source totals, and complete acceptance. Demo checks validate demo files only; client data needs equivalent contract checks and source-owner sign-off.

## Private sharing and refresh

Publish to a private Power BI workspace only after acceptance. Configure workspace membership, semantic-model permissions and any required row-level security for that client; this collection does not include a universal security policy. Do not use public Publish to web for confidential data.

Folder mode points to a local path. A Service refresh generally needs an appropriate gateway and accessible folder, or an intentionally replaced source such as SharePoint, SQL or a dataflow. Credentials, refresh schedules and deployment are configured in the customer's environment, not embedded here. Check current Microsoft licensing and capacity requirements for the chosen sharing arrangement.

## Troubleshooting

| Symptom | Check |
|---|---|
| PBIP cannot open | Current standard Desktop, relevant options, intact folder layout, short extracted path |
| File not found after refresh | DataMode, absolute DataFolder, every required CSV and exact filename |
| Type-conversion error | ISO dates, numeric decimals, blank nullable dates and CSV quoting |
| Blank visuals | Refresh completed, filters cleared, matching keys and date coverage |
| Reconciliation differs | Clear filters, compare correct period/snapshot and run the supplied DAX query |
| Headcount seems lower than sum of rows | The metric intentionally uses the latest selected month |
| CRM won values differ from monthly bookings | Month filters use creation cohorts, not closing dates |
| Cash differs from profit | Separate accounting bases; compare their respective source ledgers |

## Distributable PBIX

After the project opens, refreshes and passes reconciliation, save a copy as `.pbix` in Desktop. Review whether that copy contains real data before sharing. The source collection itself contains no prebuilt PBIX binary.
