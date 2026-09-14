"""Database access helpers for invoice workflow stages."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import Invoice


def get_invoice(session: Session, invoice_id: int) -> Invoice | None:
    return session.get(Invoice, invoice_id)


def list_invoices(
    session: Session,
    *,
    status: str | None = None,
    limit: int = 100,
) -> list[Invoice]:
    """Return invoices ordered by newest database id first."""
    if limit < 1 or limit > 500:
        raise ValueError("limit must be between 1 and 500")

    statement = select(Invoice).order_by(Invoice.invoice_id.desc()).limit(limit)
    if status is not None:
        statement = statement.where(Invoice.status == status)
    return list(session.scalars(statement))
