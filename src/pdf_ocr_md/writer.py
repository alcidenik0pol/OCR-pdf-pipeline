from __future__ import annotations

from pathlib import Path

from .transform import PageAnalysis, build_fallback_aggregate, build_page_markdown


def output_markdown_path(pdf_path: Path, output_dir: Path | None = None) -> Path:
    target_dir = output_dir if output_dir is not None else pdf_path.parent
    return target_dir / f"{pdf_path.stem}.md"


def build_document_markdown(
    source_pdf_name: str,
    page_analyses: list[PageAnalysis],
    cleaned_aggregate: str | None,
) -> str:
    sections: list[str] = [f"# OCR Transcript: {source_pdf_name}"]

    sections.append("## Clean Aggregate")
    sections.append(cleaned_aggregate.strip() if cleaned_aggregate else build_fallback_aggregate(page_analyses))

    sections.append("## Per-Slide Details")
    for page in page_analyses:
        sections.append(build_page_markdown(page))

    return "\n\n".join(section.strip() for section in sections if section.strip()) + "\n"


def write_document_markdown(
    pdf_path: Path,
    page_analyses: list[PageAnalysis],
    cleaned_aggregate: str | None,
    output_dir: Path | None = None,
) -> Path:
    output_path = output_markdown_path(pdf_path, output_dir=output_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    content = build_document_markdown(
        source_pdf_name=pdf_path.name,
        page_analyses=page_analyses,
        cleaned_aggregate=cleaned_aggregate,
    )
    output_path.write_text(content, encoding="utf-8")
    return output_path
