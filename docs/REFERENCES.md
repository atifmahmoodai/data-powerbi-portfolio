# Format references and validation boundary

Microsoft documentation reviewed 30 September 2026:

- [Power BI Desktop projects](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview): project entry points and source folders.
- [Project report folder](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report): PBIR report definitions, resources and dataset references.
- [Project semantic model folder](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset): editable model definition formats.
- [Microsoft JSON schemas](https://github.com/microsoft/json-schemas): schema revision `24ce2795f9fb15655f61185246b6578536ca43f8` used for reproducible source validation.

The collection uses model.bim (TMSL) for semantic model metadata and PBIR JSON for report pages. Model and report paths are relative. PBIP format support and any preview settings depend on the installed Desktop release.

Schema checks cover JSON documents that declare Microsoft PBIP/PBIR/PBISM schemas. They do not execute M or DAX, validate all model.bim engine semantics, or guarantee rendering of visual properties. Custom-theme JSON is parsed but not validated against a separate theme schema. Binding and business-data checks provide additional independent coverage, with remaining Desktop checks listed in ACCEPTANCE.md.
