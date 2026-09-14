from decimal import Decimal


def test_invoice_amount_variance_calculation() -> None:
    """Validate the calculation used later by the deterministic rules engine."""
    po_amount = Decimal("10000.00")
    invoice_amount = Decimal("11500.00")
    variance = abs(invoice_amount - po_amount) / po_amount

    assert variance == Decimal("0.15")
    assert variance > Decimal("0.05")
