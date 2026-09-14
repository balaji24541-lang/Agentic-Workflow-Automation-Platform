from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api.main import app
from database.models import Base, Invoice
from database.session import get_db


def test_invoice_endpoint_returns_persisted_records() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    def override_get_db():
        with Session(engine) as session:
            session.add(
                Invoice(
                    invoice_number="INV-100",
                    amount="250.00",
                    source_dataset="test",
                    source_file="invoice-100.json",
                    status="INGESTED",
                )
            )
            session.commit()
            yield session

    app.dependency_overrides[get_db] = override_get_db
    try:
        response = TestClient(app).get("/invoices?status=INGESTED")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body[0]["invoice_number"] == "INV-100"
    assert body[0]["amount"] == "250.00"
    assert body[0]["status"] == "INGESTED"
