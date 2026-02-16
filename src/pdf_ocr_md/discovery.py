from __future__ import annotations

from pathlib import Path


def find_root_pdfs(root: Path) -> list[Path]:
    """Return PDFs in root directory only (non-recursive), sorted by name."""
    if not root.exists() or not root.is_dir():
        return []

    pdfs = [
        item
        for item in root.iterdir()
        if item.is_file() and item.suffix.lower() == ".pdf" and not item.name.startswith(".")
    ]
    return sorted(pdfs, key=lambda p: p.name.lower())
