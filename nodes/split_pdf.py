"""Example extension node: splits a PDF into one file per page.

Shared pypdf logic lives in `_pdf.py` and is imported as a sibling (Phase 2
multi-file packages). See docs/guide/creating-extensions.md.
"""

from pathlib import Path

from nodes.registry import FieldSpec, NodeSpec, register

from ._pdf import split_pdf_pages


def exec_split_pdf(params, ctx):
    file_path = Path(str(params.get("filePath", "")))
    if not file_path.is_file():
        raise ValueError(f"file not found: {file_path}")

    output_dir = str(params.get("outputDir", "")).strip()
    if not output_dir:
        output_dir = str((ctx.ext or {}).get("defaultOutputDir") or "").strip()
    if not output_dir:
        raise ValueError("outputDir is required (or set Default Output Folder in extension settings)")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_paths = split_pdf_pages(file_path, output_dir)
    return {"outputDir": str(output_dir), "pageCount": len(output_paths), "files": output_paths}


register(
    NodeSpec(
        type="acme_split_pdf",
        category="pdf",
        label="Split PDF",
        description="Splits a PDF into one file per page.",
        icon_name="FileOutput",
        default_params={"filePath": "", "outputDir": ""},
        fields=[
            FieldSpec("filePath", "PDF File", "file", file_extensions=["pdf"]),
            FieldSpec("outputDir", "Output Folder", "text", placeholder="C:\\docs\\split"),
        ],
        executor=exec_split_pdf,
        requires_exclusive_input=False,
        produces_file_output="outputDir",
    )
)
