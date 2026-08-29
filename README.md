# Acme PDF Tools (example extension)

A real, working extension — adds **Merge PDF** and **Split PDF** node types,
a Phase 3 **Default Output Folder** setting, and a Phase 4 **PDF Inspector**
sidebar page. Meant as a worked example to read alongside
[docs/guide/creating-extensions.md](../../../docs/guide/creating-extensions.md),
not as a production-grade PDF toolkit.

## Try it

1. Sidebar → **Extensions** → **Install from file...**
2. Pick `../pdf-tools.aosext` (the pre-built package, sibling to this
   directory) — or zip this directory yourself: `manifest.json`, `nodes/`,
   and `actions/` go at the zip's root, no wrapping folder.
3. Confirm the trust warning. `pypdf==4.2.0` installs into this extension's
   private `deps/` folder.
4. Optionally set **Default Output Folder** on the extension card (used when
   a node's output path is left blank).
5. **Merge PDF** and **Split PDF** appear in the palette's "pdf" category.
6. Sidebar → **Extensions** group → **PDF Inspector** — enter a PDF path and
   Inspect to see page count / metadata / sizes.

## What each file does

- **`nodes/_pdf.py`**: shared pypdf helpers (not listed in `nodeModules`).
- **Merge PDF** / **Split PDF**: relative-import the helper; fall back to
  `ctx.ext["defaultOutputDir"]` when output fields are empty.
- **`actions/inspect.py`**: Phase 4 action(s) that return a view-spec JSON
  for the PDF Inspector page (`inspect-view` + `inspect`).

Phase 2 loads each extension as `aos_ext_acme_pdf_tools` so sibling imports
work. Phase 3 settings are edited on the Extensions page and available as
`{{ ext.defaultOutputDir }}` / `ctx.ext`. Phase 4 pages appear in the
sidebar when the extension is enabled.
