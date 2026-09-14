"""Download and normalize the public Zenodo invoice/receipt annotations.

The source dataset is Cruz & Castelli (2022), DOI 10.5281/zenodo.6371710.
The large image archive is intentionally not committed to this repository.
"""

from __future__ import annotations

import argparse
import json
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.request import urlopen

DATASET_URL = "https://zenodo.org/records/6371710"
ANNOTATION_ARCHIVE_URL = (
    "https://zenodo.org/records/6371710/files/2_Annotations_Json.zip?download=1"
)
IMAGE_ARCHIVE_URL = (
    "https://zenodo.org/records/6371710/files/1_Images.zip?download=1"
)

RAW_DIR = Path("data/raw/zenodo_invoices")
PROCESSED_DIR = Path("data/processed")


@dataclass(frozen=True)
class InvoiceAnnotation:
    """Canonical fields used by the downstream invoice workflow."""

    source_file: str
    seller_name: str | None = None
    seller_address: str | None = None
    seller_tax_id: str | None = None
    buyer_tax_id: str | None = None
    invoice_date: str | None = None
    invoice_total_amount: str | None = None
    invoice_tax_amount: str | None = None
    document_reference: str | None = None


FIELD_ALIASES = {
    "seller_name": {"seller_name", "sellername", "seller"},
    "seller_address": {"seller_address", "selleraddress"},
    "seller_tax_id": {"seller_tax_id", "sellertaxid", "seller_tax_identification"},
    "buyer_tax_id": {"buyer_tax_id", "buyertaxid", "buyer_tax_identification"},
    "invoice_date": {"invoice_date", "invoicedate", "date"},
    "invoice_total_amount": {
        "invoice_total_amount",
        "invoicetotalamount",
        "invoice_total",
        "total",
    },
    "invoice_tax_amount": {
        "invoice_tax_amount",
        "invoicetaxamount",
        "invoice_tax",
        "tax",
    },
    "document_reference": {
        "document_reference",
        "documentreference",
        "reference",
        "invoice_number",
    },
}


def _normalize_key(value: str) -> str:
    return "".join(character for character in value.lower() if character.isalnum())


def _flatten_scalars(value: object, output: dict[str, str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if isinstance(child, (str, int, float)) and key not in output:
                output[key] = str(child)
            else:
                _flatten_scalars(child, output)
    elif isinstance(value, list):
        for child in value:
            _flatten_scalars(child, output)


def normalize_annotation(payload: dict[str, object], source_file: str) -> InvoiceAnnotation:
    """Map the source JSON into stable application-level field names."""
    flattened: dict[str, str] = {}
    _flatten_scalars(payload, flattened)
    normalized = {_normalize_key(key): value for key, value in flattened.items()}

    values: dict[str, str | None] = {}
    for canonical, aliases in FIELD_ALIASES.items():
        values[canonical] = next(
            (normalized[_normalize_key(alias)] for alias in aliases if _normalize_key(alias) in normalized),
            None,
        )

    return InvoiceAnnotation(source_file=source_file, **values)


def download_file(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        return
    with urlopen(url, timeout=60) as response, destination.open("wb") as output:
        output.write(response.read())


def extract_annotations(archive: Path, destination: Path = RAW_DIR / "annotations") -> int:
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as bundle:
        bundle.extractall(destination)
        return sum(1 for name in bundle.namelist() if name.lower().endswith(".json"))


def normalize_annotations(source_dir: Path = RAW_DIR / "annotations") -> list[InvoiceAnnotation]:
    records: list[InvoiceAnnotation] = []
    for path in sorted(source_dir.rglob("*.json")):
        with path.open("r", encoding="utf-8") as source:
            payload = json.load(source)
        if isinstance(payload, dict):
            records.append(normalize_annotation(payload, path.name))
    return records


def write_manifest(records: list[InvoiceAnnotation], destination: Path = PROCESSED_DIR / "invoice_annotations.jsonl") -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as output:
        for record in records:
            output.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download and normalize Zenodo invoice annotations.")
    parser.add_argument("--download-images", action="store_true", help="Download the 410 MB image archive too.")
    args = parser.parse_args()

    annotation_archive = RAW_DIR / "2_Annotations_Json.zip"
    download_file(ANNOTATION_ARCHIVE_URL, annotation_archive)
    extracted = extract_annotations(annotation_archive)
    records = normalize_annotations()
    write_manifest(records)

    if args.download_images:
        download_file(IMAGE_ARCHIVE_URL, RAW_DIR / "1_Images.zip")

    print(f"Extracted {extracted} JSON files; normalized {len(records)} records.")


if __name__ == "__main__":
    main()
