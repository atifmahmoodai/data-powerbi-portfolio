# Sales CRM Analytics Dashboard

Review open pipeline, cohort win rates, deal velocity and stale follow-up opportunities.

**Status:** implemented PBIP/PBIR source with synthetic demo data. Windows Power BI Desktop open/refresh, DAX evaluation, rendered appearance and Service deployment have not been executed. Not yet a client-certified release or exported PBIX.

## Open

1. Download/extract the Astra repository to a short Windows path.
2. Open `Dashboard.pbip` in current Power BI Desktop. Enable PBIP/PBIR options if your release requires them, then restart.
3. Click **Refresh**. `DataMode = Demo` uses embedded fixtures and requires no data-file path or account.
4. Review the three report tabs; use the dropdown filters and select chart categories to explore.
5. Run `Model.SemanticModel/DAXQueries/Reconcile.dax` in DAX query view and compare against `validation/expected-demo.json`.

## Report pages

- **Pipeline overview:** Open Pipeline, Weighted Pipeline, Open Opportunities, Stale Open Deals
- **Wins and conversion:** Won Deals, Won Value, Win Rate, Average Sales Cycle
- **Follow-up priorities:** Stale Open Deals, Stale Pipeline, Open Opportunities, Weighted Pipeline

### Page guidance

- **Pipeline overview:** Weighted pipeline applies stage probabilities as a planning heuristic, not a calibrated forecast.
- **Wins and conversion:** Monthly results use opportunity creation date. Win rate excludes open opportunities.
- **Follow-up priorities:** Stale means no recorded activity for more than 14 days as of 30 Sep 2026.

## Business scope

Creation-date cohorts; current stage/activity snapshot at 30 Sep 2026.

Month means CreatedDate, not ClosedDate. Stage histories and historical pipeline are unavailable. ClosedDate is required for Won/Lost and blank for open stages. Probability lies in [0,1]. Update fixed as-of DATE in stale-deal measures for a new reporting snapshot. No personal customer data is included.

## KPI definitions

| Metric | Definition |
|---|---|
| Opportunities | Count of opportunities created in the selected cohort. |
| Open Opportunities | Currently open opportunities in the creation cohort. |
| Open Pipeline | Current amount of open opportunities. |
| Weighted Pipeline | Open amount × stage probability; heuristic, not a calibrated forecast. |
| Won Deals | Won opportunities in the selected creation cohort. |
| Lost Deals | Lost opportunities in the selected creation cohort. |
| Won Value | Won deal amount; bookings, not recognized accounting revenue. |
| Win Rate | Wins divided by wins plus losses; excludes open deals. |
| Average Won Deal | Won value / won count. |
| Average Sales Cycle | Mean creation-to-close days for wins. |
| Stale Open Deals | Open deals with no activity for more than 14 days at the demo as-of date. |
| Stale Pipeline | Amount of stale open deals at the demo as-of date. |

## Connect customer data

Copy `data/import-template/*.csv` to a private folder and fill every required table using [DATA-CONTRACT.md](DATA-CONTRACT.md). The demo CSVs provide populated examples. In Transform data → Manage parameters set `DataMode` to `Folder` and `DataFolder` to that folder. Keep `Metrics.csv` with its supplied single row. Refresh and reconcile source totals before delivery. Expand Calendar to cover every transaction date and relevant comparison period. Do not commit customer data here.

See [shared setup](../docs/SETUP.md) and [acceptance checklist](../docs/ACCEPTANCE.md). Model relationships, Power Query and DAX are editable source files. The builder overwrites generated artifacts; preserve Desktop edits before rebuilding.
