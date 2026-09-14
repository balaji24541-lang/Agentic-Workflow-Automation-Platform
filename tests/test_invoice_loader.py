from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from database.models import Base, Invoice
from ingestion.load_invoices import load_manifest


def test_load_manifest_inserts_and_skips_duplicates(tmp_path: Path) -> None:
    manifest = tmp_path / "invoice_annotations.jsonl"
    manifest.write_text(
        '{"source_file":"a.json","seller_name":"Supplier A","invoice_total_amount":"123.45","invoice_tax_amount":"23.45","document_reference":"INV-001"}\n'
        '{"source_file":"b.json","seller_name":"Supplier B","invoice_total_amount":"88.50","document_reference":"INV-002"}\n',
        encoding="utf-8",
    )

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        inserted, skipped = load_manifest(manifest, session)
        assert (inserted, skipped) == (2, 0)

        inserted, skipped = load_manifest(manifest, session)
        assert (inserted, skipped) == (0, 2)

        invoices = session.scalars(select(Invoice).order_by(Invoice.invoice_id)).all()
        assert len(invoices) == 2
        assert invoices[0].invoice_number == "INV-001"
        assert str(invoices[0].amount) == "123.45"
        assert invoices[0].seller_name == "Supplier A"
        assert invoices[0].source_dataset == "zenodo_invoice_receipts"


def test_load_manifest_rejects_missing_source_file(tmp_path: Path) -> None:
    manifest = tmp_path / "invalid.jsonl"
    manifest.write_text('{"seller_name":"Supplier A"}\n', encoding="utf-8")

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        try:
            load_manifest(manifest, session)
        except ValueError as exc:
            assert "source_file" in str(exc)
        else:
            raise AssertionError("Expected ValueError for missing source_file")
