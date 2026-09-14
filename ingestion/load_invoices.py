"""Load the normalized public invoice manifest into PostgreSQL.

The loader is deliberately idempotent: the same source dataset/file pair is
never inserted twice. It does not invent vendor, purchase-order, or approval
relationships that are absent from the source data.
"""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import Invoice
from database.session import SessionLocal

DEFAULT_MANIFEST = Path("data/processed/invoice_annotations.jsonl")
SOURCE_DATASET = "zenodo_invoice_receipts"


def _decimal_or_none(value: str | None) -> Decimal | None:
    if value is None or not value.strip():
        return None
    normalized = value.strip().replace(",", "")
    try:
        return Decimal(normalized)
    except InvalidOperation:
        return None


def load_manifest(path: Path, session: Session, source_dataset: str = SOURCE_DATASET) -> tuple[int, int]:
    """Insert new records and return (inserted, skipped)."""
    inserted = 0
    skipped = 0

    with path.open("r", encoding="utf-8") as source:
        for line_number, line in enumerate(source, start=1):
            if not line.strip():
                continue

            payload = json.loads(line)
            source_file = payload.get("source_file")
            if not source_file:
                raise ValueError(f"Missing source_file on manifest line {line_number}")

            existing = session.scalar(
                select(Invoice).where(
                    Invoice.source_dataset == source_dataset,
                    Invoice.source_file == source_file,
                )
            )
            if existing is not None:
                skipped += 1
                continue

            invoice = Invoice(
                invoice_number=payload.get("document_reference") or source_file,
                amount=_decimal_or_none(payload.get("invoice_total_amount")),
                tax_amount=_decimal_or_none(payload.get("invoice_tax_amount")),
                invoice_date=payload.get("invoice_date"),
                seller_name=payload.get("seller_name"),
                seller_address=payload.get("seller_address"),
                seller_tax_id=payload.get("seller_tax_id"),
                buyer_tax_id=payload.get("buyer_tax_id"),
                source_dataset=source_dataset,
                source_file=source_file,
                raw_payload=payload,
                status="INGESTED",
            )
            session.add(invoice)
            inserted += 1

    session.commit()
    return inserted, skipped


def main() -> None:
    parser = argparse.ArgumentParser(description="Load normalized invoices into PostgreSQL.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()

    with SessionLocal() as session:
        inserted, skipped = load_manifest(args.manifest, session)

    print(f"Inserted {inserted} invoices; skipped {skipped} already-ingested records.")


if __name__ == "__main__":
    main()
