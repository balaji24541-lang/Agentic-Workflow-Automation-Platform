import json

from ingestion.zenodo_invoice_loader import load_annotations


def test_load_annotations_reads_public_dataset_records(tmp_path) -> None:
    annotation_dir = tmp_path / "annotations"
    annotation_dir.mkdir()
    (annotation_dir / "invoice_001.json").write_text(
        json.dumps({"invoice_total": "123.45"}), encoding="utf-8"
    )

    records = load_annotations(tmp_path)

    assert len(records) == 1
    assert records[0]["source_file"] == "invoice_001.json"
    assert records[0]["annotation"]["invoice_total"] == "123.45"
