# Real Invoice Ingestion

The project uses the public **Dataset of invoices and receipts including annotation of relevant fields** by Francisco Cruz and Mauro Castelli, published on Zenodo.

- DOI: `10.5281/zenodo.6371710`
- Source: https://zenodo.org/records/6371710
- Dataset contents: 813 invoice/receipt images plus field annotations.
- The source page lists separate archives for images and JSON annotations.

## Local download

The annotation archive is downloaded by default because it is small. The image archive is approximately 410 MB and is optional.

```bash
python -m ingestion.zenodo_invoice_dataset
```

To download the image archive too:

```bash
python -m ingestion.zenodo_invoice_dataset --download-images
```

Downloaded source data is kept under `data/raw/` and processed manifests under `data/processed/`; neither is committed to Git.

## Canonical fields

The ingestion layer normalizes source annotations into:

- seller name
- seller address
- seller tax ID
- buyer tax ID
- invoice date
- invoice total amount
- invoice tax amount
- document reference

The raw source remains the source of truth. Normalization only creates a stable internal schema for later database and agent processing.

## Citation

Cruz, F., & Castelli, M. (2022). *Dataset of invoices and receipts including annotation of relevant fields* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.6371710
