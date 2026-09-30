# Inventory & Stock Ageing Analytics

Find ageing inventory, reserved stock and warehouse capital exposure at receipt-lot level.

**Status:** implemented PBIP/PBIR source with synthetic demo data. Windows Power BI Desktop open/refresh, DAX evaluation, rendered appearance and Service deployment have not been executed. Not yet a client-certified release or exported PBIX.

## Open

1. Download/extract the Astra repository to a short Windows path.
2. Open `Dashboard.pbip` in current Power BI Desktop. Enable PBIP/PBIR options if your release requires them, then restart.
3. Click **Refresh**. `DataMode = Demo` uses embedded fixtures and requires no data-file path or account.
4. Review the three report tabs; use the dropdown filters and select chart categories to explore.
5. Run `Model.SemanticModel/DAXQueries/Reconcile.dax` in DAX query view and compare against `validation/expected-demo.json`.

## Report pages

- **Stock overview:** Stock Value, Available Units, Aged Value, Weighted Stock Age
- **Ageing exposure:** Aged Units, Aged Value, Aged Value Share, Weighted Stock Age
- **Availability and lots:** On Hand Units, Reserved Units, Available Value, Occupied Lots

## Business scope

Single stock snapshot at 30 Sep 2026; age measured from lot receipt.

Do not sum multiple snapshots. LotID is unique; 0 <= Reserved <= OnHand; UnitCost >= 0; ReceiptDate <= SnapshotDate; AgeDays must match date difference. Ageing is not a demand or reorder calculation.

## KPI definitions

| Metric | Definition |
|---|---|
| On Hand Units | Sum of OnHand at the recorded grain. |
| Reserved Units | Sum of Reserved at the recorded grain. |
| Available Units | Physical stock less reservations. |
| Stock Value | Physical stock valued at lot unit cost. |
| Available Value | Unreserved stock valued at cost. |
| Aged Units | Stock received more than 90 days before the snapshot. |
| Aged Value | Value of stock older than 90 days. |
| Aged Value Share | Aged value / all selected stock value. |
| Weighted Stock Age | Unit-weighted age of on-hand stock. |
| Occupied Lots | Lots with positive physical stock. |
| Reserved Share | Reserved units / on-hand units. |
| Product Count | Distinct products represented in selected snapshot lots. |

## Connect customer data

Copy `data/import-template/*.csv` to a private folder and fill every required table using [DATA-CONTRACT.md](DATA-CONTRACT.md). The demo CSVs provide populated examples. In Transform data → Manage parameters set `DataMode` to `Folder` and `DataFolder` to that folder. Keep `Metrics.csv` with its supplied single row. Refresh and reconcile source totals before delivery. Expand Calendar to cover every transaction date and relevant comparison period. Do not commit customer data here.

See [shared setup](../docs/SETUP.md) and [acceptance checklist](../docs/ACCEPTANCE.md). Model relationships, Power Query and DAX are editable source files. The builder overwrites generated artifacts; preserve Desktop edits before rebuilding.
