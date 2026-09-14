from pathlib import Path

import pytest

from ingestion.document_extractor import extract_text


def test_extract_text_file(tmp_path: Path) -> None:
    path = tmp_path / "invoice.txt"
    path.write_text("Invoice 123\nTotal 100.00", encoding="utf-8")
    assert extract_text(path) == "Invoice 123\nTotal 100.00"


def test_extract_text_rejects_unknown_type(tmp_path: Path) -> None:
    path = tmp_path / "invoice.csv"
    path.write_text("invoice,total\n123,100", encoding="utf-8")
    with pytest.raises(ValueError, match="Unsupported document type"):
        extract_text(path)
