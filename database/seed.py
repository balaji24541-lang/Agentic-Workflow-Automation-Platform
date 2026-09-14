"""Deprecated compatibility module.

Synthetic enterprise-data generation was intentionally removed from this project.
Public source data is ingested through modules under ``ingestion/`` instead.
"""


def main() -> None:
    raise RuntimeError(
        "Synthetic database seeding has been removed. "
        "Use ingestion.zenodo_invoice_loader for public invoice data."
    )


if __name__ == "__main__":
    main()
