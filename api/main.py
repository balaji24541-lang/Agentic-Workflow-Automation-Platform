from fastapi import Depends, FastAPI, Query
from sqlalchemy.orm import Session

from database.invoice_repository import list_invoices
from database.session import get_db

app = FastAPI(
    title="Agentic Workflow Automation Platform",
    version="0.1.0",
    description="Enterprise-oriented invoice workflow automation platform.",
)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Return a simple service health response."""
    return {"status": "ok"}


@app.get("/invoices", tags=["invoices"])
def invoices(
    status: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> list[dict[str, object | None]]:
    """Return persisted invoices for downstream review and agent stages."""
    records = list_invoices(db, status=status, limit=limit)
    return [
        {
            "invoice_id": invoice.invoice_id,
            "invoice_number": invoice.invoice_number,
            "amount": str(invoice.amount) if invoice.amount is not None else None,
            "tax_amount": str(invoice.tax_amount) if invoice.tax_amount is not None else None,
            "invoice_date": invoice.invoice_date,
            "seller_name": invoice.seller_name,
            "seller_tax_id": invoice.seller_tax_id,
            "source_dataset": invoice.source_dataset,
            "source_file": invoice.source_file,
            "status": invoice.status,
        }
        for invoice in records
    ]
