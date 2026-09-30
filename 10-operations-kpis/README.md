# Operations & Management KPI Dashboard

Track current backlog, on-time completion, service cycle time, rework and delivery cost.

**Status:** implemented PBIP/PBIR source with synthetic demo data. Windows Power BI Desktop open/refresh, DAX evaluation, rendered appearance and Service deployment have not been executed. Not yet a client-certified release or exported PBIX.

## Open

1. Download/extract the Astra repository to a short Windows path.
2. Open `Dashboard.pbip` in current Power BI Desktop. Enable PBIP/PBIR options if your release requires them, then restart.
3. Click **Refresh**. `DataMode = Demo` uses embedded fixtures and requires no data-file path or account.
4. Review the three report tabs; use the dropdown filters and select chart categories to explore.
5. Run `Model.SemanticModel/DAXQueries/Reconcile.dax` in DAX query view and compare against `validation/expected-demo.json`.

## Report pages

- **Management scorecard:** Jobs Created, Open Jobs, On Time Rate, First Pass Yield
- **Backlog and service:** Open Jobs, Overdue Open Jobs, Average Cycle Days, Completion Rate
- **Quality and cost:** Rework Jobs, Rework Rate, Recorded Cost, Cost per Completed Job

### Page guidance

- **Management scorecard:** Monthly results group jobs by creation date and show current status; they are not completion-date throughput.
- **Backlog and service:** Filter Status to Open. Overdue means the due date was before 30 Sep 2026; this is a calendar-date SLA.
- **Quality and cost:** Recorded cost includes open and completed jobs. Cost per completed job includes completed work only.

## Business scope

Creation-date cohorts and current job status at 30 Sep 2026.

Month means CreatedDate. CompletedDate is required for Completed and blank for Open. OnTime and Rework are 0/1 and zero for open jobs. CompletedDate >= CreatedDate; CycleDays must match. DueDate is a calendar-date SLA, not business-hour SLA. Update as-of DATE in overdue measure when using a newer snapshot. Historical backlog and completion-date throughput need a separate event history.

## KPI definitions

| Metric | Definition |
|---|---|
| Jobs Created | Jobs in selected creation-date cohorts. |
| Completed Jobs | Currently completed jobs in selected creation cohorts. |
| Open Jobs | Current unfinished jobs in selected creation cohorts. |
| Completion Rate | Completed jobs / created jobs in cohort; not daily throughput. |
| On Time Jobs | Completed jobs by due date. |
| On Time Rate | Completed on-time jobs / all completed jobs. |
| Average Cycle Days | Mean creation-to-completion days for finished work. |
| Overdue Open Jobs | Open jobs whose due date precedes the demo snapshot date. |
| Rework Jobs | Completed jobs flagged for rework. |
| Rework Rate | Reworked completed jobs / completed jobs. |
| First Pass Yield | Completed without rework / all completed jobs. |
| Recorded Cost | Recorded cost incurred on all selected jobs; open jobs included. |
| Cost per Completed Job | Cost associated with completed jobs / completed count. |

## Connect customer data

Copy `data/import-template/*.csv` to a private folder and fill every required table using [DATA-CONTRACT.md](DATA-CONTRACT.md). The demo CSVs provide populated examples. In Transform data → Manage parameters set `DataMode` to `Folder` and `DataFolder` to that folder. Keep `Metrics.csv` with its supplied single row. Refresh and reconcile source totals before delivery. Expand Calendar to cover every transaction date and relevant comparison period. Do not commit customer data here.

See [shared setup](../docs/SETUP.md) and [acceptance checklist](../docs/ACCEPTANCE.md). Model relationships, Power Query and DAX are editable source files. The builder overwrites generated artifacts; preserve Desktop edits before rebuilding.
