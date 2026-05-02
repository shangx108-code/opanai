# Final submission PDFs - 2026-05-02

This folder contains the current Path A submission PDFs for the compensated-magnetic Josephson-junction topological-superconductivity manuscript.

Files:
- `main.pdf`: main manuscript PDF.
- `supplementary_information.pdf`: Supplementary Information PDF.

Because the current GitHub connector writes UTF-8 text files only, the PDFs are mirrored in this repository as recoverable Base64 files:
- `main.pdf.base64`
- `supplementary_information.pdf.base64`

Recover locally with:
```bash
base64 -d main.pdf.base64 > main.pdf
base64 -d supplementary_information.pdf.base64 > supplementary_information.pdf
sha256sum main.pdf supplementary_information.pdf
```

These files were copied from the current compiled submission artifacts and mirrored at the project root as `submission_draft_main.pdf` and `supplementary_information.pdf` for backward compatibility with earlier project paths.
