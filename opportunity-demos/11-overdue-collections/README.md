# Overdue Collections

## Decision supported

Review **invoice balance** across invoice and periods; investigate **days overdue**.

## Demo and model

- Open `index.html` in a browser for the interactive synthetic-data reference dashboard.
- `data.csv` is synthetic PKR / unit data and can be refreshed into a report model.
- `model.json` records the demo rows and metric card definitions.
- Intended data grain: one row per collection and month.
- Useful dimensions: period, invoice, item, status.
- Core measures: total invoice balance, comparison against target/cost, row-level indicator, selected-period totals.

## Power BI handoff

The browser dashboard is a working analytics prototype, not a native `.pbip` report. For a Power BI implementation, load `data.csv`, validate its grain and business definitions with the client, create the measures, and build overview, trend and exception pages in Power BI Desktop. Connect a customer source only after field mapping and KPI sign-off.

All sample data is fictional. This project is not connected to an ERP or customer system.
