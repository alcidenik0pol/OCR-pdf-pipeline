from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PageAnalysis:
    page_number: int
    retranscribed_text: str
    math_markdown: list[str] = field(default_factory=list)
    image_descriptions: list[str] = field(default_factory=list)


def _normalize_multiline(text: str) -> str:
    lines = [line.rstrip() for line in text.splitlines()]
    cleaned = "\n".join(lines).strip()
    return cleaned


def normalize_math_entries(entries: list[str]) -> list[str]:
    normalized: list[str] = []
    for entry in entries:
        cleaned = _normalize_multiline(entry)
        if not cleaned:
            continue
        if cleaned.startswith("$") and cleaned.endswith("$"):
            normalized.append(cleaned)
        else:
            normalized.append(f"$$\n{cleaned}\n$$")
    return normalized


def build_page_markdown(analysis: PageAnalysis) -> str:
    text_block = _normalize_multiline(analysis.retranscribed_text) or "(No text detected)"
    math_entries = normalize_math_entries(analysis.math_markdown)
    image_entries = [d.strip() for d in analysis.image_descriptions if d.strip()]

    parts: list[str] = [f"## Slide {analysis.page_number}"]
    parts.append("### Retranscribed Text")
    parts.append(text_block)

    parts.append("### Math")
    if math_entries:
        parts.extend(math_entries)
    else:
        parts.append("(No explicit math content detected)")

    parts.append("### Images")
    if image_entries:
        parts.extend([f"- {item}" for item in image_entries])
    else:
        parts.append("- (No meaningful image content detected)")

    return "\n\n".join(parts).strip()


def build_fallback_aggregate(pages: list[PageAnalysis]) -> str:
    chunks: list[str] = []
    for page in pages:
        text = _normalize_multiline(page.retranscribed_text)
        if text:
            chunks.append(text)
    if not chunks:
        return "(No aggregate text available)"
    return "\n\n".join(chunks)
