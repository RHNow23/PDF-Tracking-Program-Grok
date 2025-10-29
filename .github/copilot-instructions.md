## Repository purpose
This repository is a single-script utility that stores PDF files into an SQLite database and extracts searchable text using PyMuPDF (imported as `fitz`). The main script is `PDF Tracking Program Grok.py`.

## High-level architecture
- Single-file Python script (`PDF Tracking Program Grok.py`).
- Data persistence: local SQLite database created as `pdf_database.db` in the current working directory (no external DB server).
- PDF processing: uses PyMuPDF (`fitz`) to extract text from PDFs; PDFs themselves are stored as BLOBs in the DB.

## Key files to inspect
- `PDF Tracking Program Grok.py` — primary implementation: DB schema, text extraction (`extract_text_from_pdf`), store/retrieve functions, and a simple `main()` example flow.

## Developer workflows (how to run & debug)
- Create a virtual environment then install PyMuPDF in PowerShell:
  - `python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install pymupdf`
- Run the script from the repository root (PowerShell):
  - `python "PDF Tracking Program Grok.py"`
- The script creates `pdf_database.db` in the working directory. To test manually, replace the placeholder paths in `main()`:
  - `pdf_directory = "path/to/your/pdf/folder"` — change to a real folder with PDFs.
  - `output_directory = "path/to/output/folder"` — ensure the folder exists or let the script create it.

## Important patterns & conventions specific to this repo
- Single script style: No packaging, no tests, no CLI flags. Expect code to be edited directly in the file.
- DB schema: table `pdfs(id, name, data, extracted_text)`. When searching, the script uses SQL LIKE over `name` or `extracted_text`.
- Error handling: top-level functions print errors and return defaults (e.g., `extract_text_from_pdf` returns empty string on failure). Use prints for debugging.

## Integration points & external deps
- PyMuPDF (`pip install pymupdf`) — used for text extraction. Ensure version compatible with your Python runtime.
- SQLite — standard library `sqlite3`, DB file `pdf_database.db` (local file). No network connections.

## Typical change tasks & examples for an AI coding agent
- Add a CLI: update `main()` to accept paths/commands rather than hardcoded strings. Example: replace `pdf_directory = "path/to/your/pdf/folder"` with an argparse-based CLI.
- Add tests: create a small `tests/` harness that runs `store_pdf`, `search_pdfs`, and `retrieve_pdf` against a temporary SQLite file.
- Improve extraction robustness: handle encrypted PDFs and large documents via streaming/iterative reads.

## Small, safe refactors an agent can do right away
- Move DB initialization (schema SQL) into a small helper `schema.sql` or a function that returns schema constant.
- Replace prints with a lightweight logger (Python `logging`) while preserving current output behavior.

## What not to change without confirmation
- Do not change the storage format (storing PDFs as BLOBs) unless the user confirms migration plan.
- Avoid adding any network I/O or cloud storage without explicit instructions.

## Quick examples (explicit references)
- Search by name (example code location): `search_pdfs(cursor, 'example', search_type='name')` in `main()`.
- Database creation: `sqlite3.connect('pdf_database.db')` — the DB file path is relative to the working directory.

## Next steps for collaborators / agents
- If asked to add features, prefer backward-compatible changes (new CLI flags, optional logging, tests in `tests/`).
- If you need to run or test, instruct the user to supply a small sample PDF directory. For unit tests use tmpdir and a small fixture PDF.

---
If any section above is unclear or you'd like the agent to add a CLI, tests, or a migration plan (to keep PDFs on disk instead of BLOBs), tell me which item to implement next and I will update the repo accordingly.
