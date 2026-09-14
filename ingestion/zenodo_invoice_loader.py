"""Load annotated invoice/receipt records from the public Zenodo dataset.

Expected layout after downloading and extracting the public dataset:

    data/raw/invoices/
        images/...
        annotations/*.json

The loader intentionally reads the annotations rather than inventing transaction data.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_ROOT = Path("data/raw/invoices")


def load_annotations(root: Path = DEFAULT_ROOT) -> list[dict[str, Any]]:
    """Return all JSON annotation records from a downloaded dataset."""
    annotation_dir = root / "annotations"
    if not annotation_dir.exists():
        raise FileNotFoundError(
            f"Annotation directory not found: {annotation_dir}. "
            "Download the public Zenodo dataset first."
        )

    records: list[dict[str, Any]] = []
    for path in sorted(annotation_dir.glob("*.json")):
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        records.append({"source_file": path.name, "annotation": payload})

    return records


def main() -> None:
    records = load_annotations()
    print(f"Loaded {len(records)} public invoice annotations.")


if __name__ == "__main__":
    main()
