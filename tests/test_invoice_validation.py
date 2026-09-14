from analysis.invoice_validation import validate_invoice, validation_status


def test_valid_invoice_passes() -> None:
    record = {
        "seller_name": "Supplier A",
        "document_reference": "INV-1",
        "invoice_total_amount": "100.00",
        "invoice_tax_amount": "18.00",
    }
    assert validate_invoice(record) == []
    assert validation_status([]) == "PASS"


def test_missing_reference_requires_review() -> None:
    record = {
        "seller_name": "Supplier A",
        "invoice_total_amount": "100.00",
        "invoice_tax_amount": "18.00",
    }
    issues = validate_invoice(record)
    assert any(issue.rule == "REFERENCE_REQUIRED" for issue in issues)
    assert validation_status(issues) == "REVIEW"


def test_tax_cannot_exceed_total() -> None:
    record = {
        "seller_name": "Supplier A",
        "document_reference": "INV-2",
        "invoice_total_amount": "100.00",
        "invoice_tax_amount": "120.00",
    }
    issues = validate_invoice(record)
    assert any(issue.rule == "TAX_NOT_GREATER_THAN_TOTAL" for issue in issues)
