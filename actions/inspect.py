"""PDF Inspector view + inspect actions (Phase 4b example)."""

from __future__ import annotations

from pathlib import Path


def _view_spec(path: str = "", extras=None):
    blocks = [
        {"type": "text", "value": "Pick a PDF to inspect. Page count and basic metadata are returned below."},
        {
            "type": "form",
            "action": "inspect",
            "submitLabel": "Inspect",
            "fields": [
                {
                    "key": "path",
                    "label": "PDF path",
                    "type": "text",
                    "placeholder": r"C:\docs\file.pdf",
                }
            ],
        },
    ]
    if extras:
        blocks.extend(extras)
    blocks.append(
        {
            "type": "button",
            "label": "Refresh",
            "action": "inspect-view",
            "payload": {},
        }
    )
    return {"title": "PDF Inspector", "blocks": blocks}


def handle(request):
    action = request.get("action") or ""
    payload = request.get("payload") or {}
    settings = request.get("extensionSettings") or {}

    if action == "inspect-view":
        return _view_spec()

    if action != "inspect":
        return _view_spec()

    path = str(payload.get("path") or "").strip()
    if not path:
        default_dir = str(settings.get("defaultOutputDir") or "").strip()
        return _view_spec(
            extras=[
                {
                    "type": "text",
                    "value": "Enter a PDF path"
                    + (f" (default folder setting: {default_dir})" if default_dir else "")
                    + ".",
                }
            ]
        )

    pdf_path = Path(path)
    if not pdf_path.is_file():
        return _view_spec(
            path,
            extras=[{"type": "text", "value": f"File not found: {path}"}],
        )

    try:
        from pypdf import PdfReader

        reader = PdfReader(str(pdf_path))
        n = len(reader.pages)
        meta = reader.metadata
        items = [
            {"label": "File", "value": str(pdf_path)},
            {"label": "Pages", "value": str(n)},
        ]
        if meta:
            if getattr(meta, "title", None):
                items.append({"label": "Title", "value": str(meta.title)})
            if getattr(meta, "author", None):
                items.append({"label": "Author", "value": str(meta.author)})

        rows = []
        for i, page in enumerate(reader.pages[:50], start=1):
            box = page.mediabox
            w = float(box.width) if box else 0
            h = float(box.height) if box else 0
            rows.append([str(i), f"{w:.0f}×{h:.0f}"])

        extras = [
            {"type": "keyValue", "items": items},
            {
                "type": "table",
                "columns": ["Page", "Size (pt)"],
                "rows": rows,
            },
        ]
        if n > 50:
            extras.append(
                {
                    "type": "text",
                    "value": f"Showing first 50 of {n} pages.",
                }
            )
        return _view_spec(path, extras=extras)
    except Exception as exc:
        return _view_spec(
            path,
            extras=[{"type": "text", "value": f"Could not read PDF: {exc}"}],
        )
