from ingestion.zenodo_invoice_dataset import normalize_annotation


def test_normalize_annotation_maps_source_fields() -> None:
    payload = {
        "seller_name": "Example Supplier",
        "seller_address": "Rua Example 1",
        "seller_tax_id": "PT123456789",
        "buyer_tax_id": "PT987654321",
        "invoice_date": "2022-03-01",
        "invoice_total_amount": "123.45",
        "invoice_tax_amount": "23.09",
        "document_reference": "FT 2022/123",
    }

    record = normalize_annotation(payload, "invoice.json")

    assert record.source_file == "invoice.json"
    assert record.seller_name == "Example Supplier"
    assert record.invoice_total_amount == "123.45"
    assert record.document_reference == "FT 2022/123"


def test_normalize_annotation_handles_nested_payloads() -> None:
    payload = {
        "document": {
            "seller": {"name": "Nested Supplier"},
            "date": "2022-03-02",
            "total": 88.50,
        }
    }

    record = normalize_annotation(payload, "nested.json")

    assert record.seller_name == "Nested Supplier"
    assert record.invoice_date == "2022-03-02"
    assert record.invoice_total_amount == "88.5"
