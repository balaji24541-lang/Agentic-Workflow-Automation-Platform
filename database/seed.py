"""Seed a realistic, repeatable invoice-processing dataset.

The generated data intentionally contains both clean and problematic cases so later
agent/validation features can be tested against known scenarios.
"""

from __future__ import annotations

import random
from decimal import Decimal

from faker import Faker
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from database.init_db import init_db
from database.models import Invoice, PurchaseOrder, Vendor
from database.session import SessionLocal

SEED = 42
VENDOR_COUNT = 25
PO_COUNT = 100
INVOICE_COUNT = 150


VENDOR_NAMES = [
    "Apex Technologies",
    "BluePeak Solutions",
    "Crescent Office Systems",
    "Delta Industrial Supply",
    "Evergreen Logistics",
    "Fusion Cloud Services",
    "Global Office Partners",
    "Horizon Telecom",
    "Innova Systems",
    "Jupiter Facilities",
]


def seed_database(session: Session) -> None:
    """Populate the database once; subsequent runs are safe and idempotent."""
    existing = session.scalar(select(func.count()).select_from(Vendor)) or 0
    if existing:
        print(f"Database already contains {existing} vendors; skipping seed.")
        return

    fake = Faker("en_IN")
    Faker.seed(SEED)
    random.seed(SEED)

    vendors: list[Vendor] = []
    for index in range(VENDOR_COUNT):
        name = VENDOR_NAMES[index] if index < len(VENDOR_NAMES) else fake.company()
        vendors.append(
            Vendor(
                name=name,
                email=fake.company_email(),
                payment_terms=random.choice(["NET-15", "NET-30", "NET-45", "NET-60"]),
                risk_score=Decimal(str(round(random.uniform(0.02, 0.75), 4))),
            )
        )

    session.add_all(vendors)
    session.flush()

    purchase_orders: list[PurchaseOrder] = []
    for index in range(PO_COUNT):
        vendor = random.choice(vendors)
        amount = Decimal(random.randint(500, 250_000)).quantize(Decimal("0.01"))
        purchase_orders.append(
            PurchaseOrder(
                vendor_id=vendor.vendor_id,
                po_number=f"PO-{2026_0000 + index:06d}",
                total_amount=amount,
                status=random.choices(["OPEN", "CLOSED"], weights=[85, 15])[0],
            )
        )

    session.add_all(purchase_orders)
    session.flush()

    invoices: list[Invoice] = []
    for index in range(INVOICE_COUNT):
        po = random.choice(purchase_orders)
        scenario = index % 10

        if scenario == 0:
            # Deliberate amount mismatch (>5%) for validation tests.
            amount = (po.total_amount * Decimal("1.15")).quantize(Decimal("0.01"))
        elif scenario == 1:
            # Deliberate missing PO reference.
            po_number = "PO-MISSING-999"
            amount = Decimal(random.randint(1_000, 50_000)).quantize(Decimal("0.01"))
            invoices.append(
                Invoice(
                    vendor_id=po.vendor_id,
                    invoice_number=f"INV-{2026_0000 + index:06d}",
                    po_number=po_number,
                    amount=amount,
                    status="PENDING",
                    raw_text="Synthetic invoice requiring PO lookup.",
                )
            )
            continue
        elif scenario == 2:
            # Deliberate high-risk vendor case.
            risky_vendor = max(vendors, key=lambda vendor: vendor.risk_score)
            po = random.choice([item for item in purchase_orders if item.vendor_id == risky_vendor.vendor_id])
            amount = po.total_amount
        else:
            amount = po.total_amount

        invoice_number = f"INV-{2026_0000 + index:06d}"
        invoices.append(
            Invoice(
                vendor_id=po.vendor_id,
                invoice_number=invoice_number,
                po_number=po.po_number,
                amount=amount,
                status="PENDING",
                raw_text="Synthetic invoice generated for workflow testing.",
            )
        )

    # Add a duplicate invoice number intentionally for duplicate-detection tests.
    duplicate_source = invoices[10]
    invoices.append(
        Invoice(
            vendor_id=duplicate_source.vendor_id,
            invoice_number=duplicate_source.invoice_number,
            po_number=duplicate_source.po_number,
            amount=duplicate_source.amount,
            status="PENDING",
            raw_text="Synthetic duplicate invoice for validation testing.",
        )
    )

    session.add_all(invoices)
    session.commit()

    print(
        f"Seed complete: {len(vendors)} vendors, "
        f"{len(purchase_orders)} purchase orders, {len(invoices)} invoices."
    )


def main() -> None:
    init_db()
    with SessionLocal() as session:
        seed_database(session)


if __name__ == "__main__":
    main()
