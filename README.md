# Power BI — Business Analytics Collection

Ten independent native Power BI projects inside the **Astra** repository. Each folder is a standalone solution that can be copied or extracted independently. These are ordinary project folders, not nested Git repositories or submodules.

**Implemented:** 10 PBIP projects, 30 PBIR report pages, 360 native visuals, 133 DAX measures, typed Power Query imports, dimensional relationships, deterministic synthetic data, customer CSV templates and setup documentation.

**Validation boundary:** source checks and Python reconciliation are automated. Power BI Desktop opening, Power Query refresh, actual DAX evaluation and rendered report appearance require Windows acceptance. No exported PBIX, customer integration, scheduled refresh or Service deployment is claimed.

## Choose a project

| # | Solution | Business decisions | Open in Power BI Desktop |
|---|---|---|---|
| 1 | [Car Dealership Profitability & Inventory](01-dealership-profitability/) | Vehicle margins, stock capital and ageing | [Dashboard.pbip](01-dealership-profitability/Dashboard.pbip) |
| 2 | [Executive Sales Performance](02-executive-sales/) | Actual versus target, customers, regions and salespeople | [Dashboard.pbip](02-executive-sales/Dashboard.pbip) |
| 3 | [Inventory & Stock Ageing](03-inventory-stock-ageing/) | Lot ageing, available stock and warehouse exposure | [Dashboard.pbip](03-inventory-stock-ageing/Dashboard.pbip) |
| 4 | [Financial P&L / Cash Flow](04-financial-pnl-cashflow/) | Profit, budget variance and separate cash movements | [Dashboard.pbip](04-financial-pnl-cashflow/Dashboard.pbip) |
| 5 | [Retail Store Performance](05-retail-performance/) | Store conversion, baskets, refunds and margin | [Dashboard.pbip](05-retail-performance/Dashboard.pbip) |
| 6 | [E-commerce Profitability](06-ecommerce-profitability/) | Contribution after refunds, fulfilment and advertising | [Dashboard.pbip](06-ecommerce-profitability/Dashboard.pbip) |
| 7 | [Sales CRM Analytics](07-sales-crm/) | Open pipeline, cohort win rates and stale deals | [Dashboard.pbip](07-sales-crm/Dashboard.pbip) |
| 8 | [HR / Workforce Analytics](08-hr-workforce/) | Staffing, attrition, absence and payroll | [Dashboard.pbip](08-hr-workforce/Dashboard.pbip) |
| 9 | [Project Profitability](09-project-profitability/) | Engagement margin, cost budgets and collections | [Dashboard.pbip](09-project-profitability/Dashboard.pbip) |
| 10 | [Operations & Management KPIs](10-operations-kpis/) | Backlog, SLA completion, quality and cost | [Dashboard.pbip](10-operations-kpis/Dashboard.pbip) |

## Start here

1. In GitHub choose **Code → Download ZIP**, then extract the entire repository.
2. Open a project's `Dashboard.pbip` using standard Power BI Desktop on Windows.
3. Click **Refresh**. The default Demo mode loads embedded synthetic data without a file-path change or login.
4. Explore its three tabs, dropdown filters and clickable charts.
5. Follow [Desktop acceptance](docs/ACCEPTANCE.md) before presenting it as a working client solution. Save As PBIX from Desktop when you need a single distributable report file.

All demo money is **PKR** and the reference snapshot is **30 September 2026**. Every report labels its data as synthetic. The models differ intentionally: inventory is a snapshot, CRM/operations use creation-date cohorts, finance separates accrual profit from cash, and HR uses latest-period headcount.

## What every project contains

- `Dashboard.pbip`, `Dashboard.Report/`, `Model.SemanticModel/`: editable Power BI report and semantic model sources.
- `data/demo/`: populated synthetic CSV examples; the same data is embedded in Power Query.
- `data/import-template/`: customer import headers, plus the required single-row Metrics file.
- `queries/`, `measures.dax`: readable Power Query and KPI definitions.
- `DATA-CONTRACT.md`, `README.md`: grain, field types, business assumptions and setup.
- `validation/expected-demo.json`, `Model.SemanticModel/DAXQueries/Reconcile.dax`: expected totals and the query to check them in Desktop.

## Develop and validate

Python 3.10+ builds the collection without third-party packages. Validation with Microsoft schemas uses the pinned development requirements.

```bash
python -m pip install -r power-bi/requirements-dev.txt
python power-bi/scripts/build.py
python -m unittest discover -s power-bi/tests -v
python power-bi/scripts/validate.py
```

For schema validation, check out Microsoft's schema repository at the documented revision:

```bash
git clone https://github.com/microsoft/json-schemas.git ../ms-schemas
git -C ../ms-schemas checkout 24ce2795f9fb15655f61185246b6578536ca43f8
python power-bi/scripts/validate.py --schemas ../ms-schemas
```

The validator writes [validation/results.json](validation/results.json). Running without `--schemas` explicitly records that schema validation was skipped. CI runs the full schema checks and detects generated-source drift.

**Rebuild warning:** `scripts/catalog.py` is the business specification and fixture source; `scripts/build.py` owns generated projects. Preserve manual Desktop edits before rebuilding. No customer data, credentials or report caches should be committed.

See [setup and deployment](docs/SETUP.md), [acceptance](docs/ACCEPTANCE.md) and [source references](docs/REFERENCES.md).
