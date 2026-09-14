from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database.invoice_repository import get_invoice, list_invoices
from database.models import Base, Invoice


def test_invoice_repository_filters_and_orders() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add_all(
            [
                Invoice(invoice_number="A", source_dataset="test", source_file="a.json", status="INGESTED"),
                Invoice(invoice_number="B", source_dataset="test", source_file="b.json", status="REVIEW"),
            ]
        )
        session.commit()

        review = list_invoices(session, status="REVIEW")
        assert [invoice.invoice_number for invoice in review] == ["B"]

        all_invoices = list_invoices(session)
        assert [invoice.invoice_number for invoice in all_invoices] == ["B", "A"]
        assert get_invoice(session, all_invoices[0].invoice_id).invoice_number == "B"
