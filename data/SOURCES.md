# Public Data Sources

This project does **not** generate synthetic enterprise transactions.

## Primary document dataset

**Dataset of invoices and receipts including annotation of relevant fields**

- Source: Zenodo, DOI `10.5281/zenodo.6371710`
- URL: https://zenodo.org/records/6371710
- Contents: 813 invoice/receipt images plus JSON annotations
- Annotated fields include seller, buyer tax IDs, invoice date, total amount, tax amount, and document reference.
- Language: Portuguese

The repository does not commit the downloaded dataset because the image archive is hundreds of megabytes. Download the dataset separately and place the extracted files under `data/raw/invoices/`.

## Procurement context

For structured public-procurement context, we use datasets from the Open Contracting Partnership Data Registry. The registry provides OCDS datasets in JSON, CSV, and Excel formats.

Recommended India source:

- Assam State Government Finance Department
- Source: https://data.open-contracting.org/en/publication/131
- License: Government Open Data License - India
- Coverage: September 2022
- Available formats: JSON, CSV, Excel

The procurement dataset is treated as a separate source unless a documented business key proves that records can be joined. We do **not** fabricate invoice-to-PO relationships.

## Reproducibility

Record the exact source URL, download date, dataset version/DOI, and license in any experiment or README update. Keep raw source data outside Git unless its redistribution terms explicitly permit repository storage.
