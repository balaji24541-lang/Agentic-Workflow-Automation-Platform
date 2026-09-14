"""Extract text from local invoice documents without inventing fields."""
from __future__ import annotations

from pathlib import Path


def extract_text(path: str | Path) -> str:
    """Extract text from a PDF or plain-text document.

    Scanned PDFs may return an empty string; OCR is deliberately handled as a
    separate capability so extraction never silently fabricates content.
    """
    source = Path(path)
    suffix = source.suffix.lower()
    if suffix in {".txt", ".text"}:
        return source.read_text(encoding="utf-8")
    if suffix == ".pdf":
        import fitz

        document = fitz.open(source)
        try:
            return "\n".join(page.get_text("text") for page in document).strip()
        finally:
            document.close()
    raise ValueError(f"Unsupported document type: {suffix or '<none>'}")
