"""Example extension node: merges multiple PDF files into one.

Written exactly like a core node module -- see docs/guide/creating-extensions.md
for the walkthrough this file is the worked example for. Shared pypdf logic
lives in `_pdf.py` and is imported as a sibling (Phase 2 multi-file packages).
"""

from pathlib import Path

from nodes.registry import FieldSpec, NodeSpec, register

from ._pdf import merge_pdf_files


def exec_merge_pdf(params, ctx):
    file_paths = [line.strip() for line in str(params.get("files", "")).splitlines() if line.strip()]
    if len(file_paths) < 2:
        raise ValueError("Merge PDF needs at least two file paths (one per line)")

    output_path = str(params.get("outputPath", "")).strip()
    if not output_path:
        default_dir = str((ctx.ext or {}).get("defaultOutputDir") or "").strip()
        if not default_dir:
            raise ValueError("outputPath is required (or set Default Output Folder in extension settings)")
        output_path = str(Path(default_dir) / "merged.pdf")
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    source_count = merge_pdf_files(file_paths, output_path)
    return {"outputPath": str(output_path), "sourceCount": source_count}


register(
    NodeSpec(
        type="acme_merge_pdf",
        category="pdf",
        label="Merge PDF",
        description="Merges multiple PDF files into one, in the order listed.",
        icon_name="FileStack",
        default_params={"files": "", "outputPath": ""},
        fields=[
            FieldSpec(
                "files", "Files to Merge (one path per line)", "textarea",
                placeholder="C:\\docs\\part1.pdf\nC:\\docs\\part2.pdf",
                hint="At least two PDF file paths, in the order they should be merged.",
            ),
            FieldSpec("outputPath", "Output File", "text", placeholder="C:\\docs\\merged.pdf"),
        ],
        executor=exec_merge_pdf,
        requires_exclusive_input=False,
        produces_file_output="outputPath",
    )
)
