"""Deterministic validation rules for extracted invoice fields."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation


@dataclass(frozen=True)
class ValidationIssue:
    rule: str
    severity: str
    message: str


def _amount(value: str | Decimal | None) -> Decimal | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        return Decimal(str(value).replace(",", "").strip())
    except (InvalidOperation, ValueError):
        return None


def validate_invoice(record: dict[str, object]) -> list[ValidationIssue]:
    """Apply explainable rules; no LLM is used for deterministic checks."""
    issues: list[ValidationIssue] = []
    total = _amount(record.get("invoice_total_amount"))
    tax = _amount(record.get("invoice_tax_amount"))

    if not record.get("seller_name"):
        issues.append(ValidationIssue("SELLER_REQUIRED", "ERROR", "Seller name is missing."))
    if not record.get("document_reference"):
        issues.append(ValidationIssue("REFERENCE_REQUIRED", "ERROR", "Document reference is missing."))
    if total is None:
        issues.append(ValidationIssue("TOTAL_REQUIRED", "ERROR", "Invoice total is missing or invalid."))
    elif total <= 0:
        issues.append(ValidationIssue("TOTAL_POSITIVE", "ERROR", "Invoice total must be greater than zero."))
    if tax is not None and tax < 0:
        issues.append(ValidationIssue("TAX_NON_NEGATIVE", "ERROR", "Invoice tax cannot be negative."))
    if total is not None and tax is not None and tax > total:
        issues.append(ValidationIssue("TAX_NOT_GREATER_THAN_TOTAL", "ERROR", "Invoice tax cannot exceed the invoice total."))

    return issues


def validation_status(issues: list[ValidationIssue]) -> str:
    return "REVIEW" if any(issue.severity == "ERROR" for issue in issues) else "PASS"
