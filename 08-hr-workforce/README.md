# HR / Workforce Analytics System

Monitor staffing, period attrition, attendance and payroll without double-counting monthly headcount.

**Status:** implemented PBIP/PBIR source with synthetic demo data. Windows Power BI Desktop open/refresh, DAX evaluation, rendered appearance and Service deployment have not been executed. Not yet a client-certified release or exported PBIX.

## Open

1. Download/extract the Astra repository to a short Windows path.
2. Open `Dashboard.pbip` in current Power BI Desktop. Enable PBIP/PBIR options if your release requires them, then restart.
3. Click **Refresh**. `DataMode = Demo` uses embedded fixtures and requires no data-file path or account.
4. Review the three report tabs; use the dropdown filters and select chart categories to explore.
5. Run `Model.SemanticModel/DAXQueries/Reconcile.dax` in DAX query view and compare against `validation/expected-demo.json`.

## Report pages

- **Workforce overview:** Headcount, Hires, Leavers, Period Attrition
- **Retention and hiring:** Average Opening Headcount, Hires, Net Hiring, Period Attrition
- **Attendance and cost:** Payroll, Payroll per Employee Month, Absence Rate, Overtime Hours

## Business scope

Jan–Sep 2026 department/month snapshots; headcount uses latest selected month.

ClosingHeadcount = OpeningHeadcount + Hires - Leavers. Next month opening equals prior closing. All departments must have the same month coverage. AbsentHours <= ScheduledHours. Aggregate, synthetic HR data only; access controls for real employee information must be designed before deployment.

## KPI definitions

| Metric | Definition |
|---|---|
| Headcount | Closing headcount at the latest snapshot in the selected period; never sum months. |
| Average Opening Headcount | Average of selected monthly opening headcounts. |
| Hires | Sum of Hires at the recorded grain. |
| Leavers | Sum of Leavers at the recorded grain. |
| Net Hiring | Period hires less leavers. |
| Period Attrition | Leavers in selected months / average monthly opening headcount. Period rate, not annualized. |
| Scheduled Hours | Sum of ScheduledHours at the recorded grain. |
| Absent Hours | Sum of AbsentHours at the recorded grain. |
| Absence Rate | Absent hours / scheduled hours. |
| Overtime Hours | Sum of OvertimeHours at the recorded grain. |
| Payroll | Total payroll over selected months. |
| Payroll per Employee Month | Payroll / sum of monthly closing headcounts; employee-month cost, not payroll / latest headcount. |

## Connect customer data

Copy `data/import-template/*.csv` to a private folder and fill every required table using [DATA-CONTRACT.md](DATA-CONTRACT.md). The demo CSVs provide populated examples. In Transform data → Manage parameters set `DataMode` to `Folder` and `DataFolder` to that folder. Keep `Metrics.csv` with its supplied single row. Refresh and reconcile source totals before delivery. Expand Calendar to cover every transaction date and relevant comparison period. Do not commit customer data here.

See [shared setup](../docs/SETUP.md) and [acceptance checklist](../docs/ACCEPTANCE.md). Model relationships, Power Query and DAX are editable source files. The builder overwrites generated artifacts; preserve Desktop edits before rebuilding.
