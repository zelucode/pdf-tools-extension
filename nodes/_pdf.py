"""Shared pypdf helpers for the Acme PDF Tools example extension.

Phase 2 loads each extension as a real package (`aos_ext_acme_pdf_tools`),
so sibling node modules can import this file via a relative import:

    from ._pdf import merge_pdf_files, split_pdf_pages
"""

from pathlib import Path


def merge_pdf_files(file_paths, output_path: Path) -> int:
    from pypdf import PdfWriter  # imported lazily -- optional dep

    writer = PdfWriter()
    for file_path in file_paths:
        writer.append(file_path)
    with open(output_path, "wb") as f:
        writer.write(f)
    return len(file_paths)


def split_pdf_pages(file_path: Path, output_dir: Path) -> list:
    from pypdf import PdfReader, PdfWriter

    reader = PdfReader(str(file_path))
    output_paths = []
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        page_path = output_dir / f"{file_path.stem}_page_{i + 1}.pdf"
        with open(page_path, "wb") as f:
            writer.write(f)
        output_paths.append(str(page_path))
    return output_paths
