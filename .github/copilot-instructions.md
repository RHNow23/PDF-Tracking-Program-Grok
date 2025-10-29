## Purpose
This repository is a small, single-file utility that stores PDF files in an SQLite database and extracts searchable text using PyMuPDF (imported as `fitz`). The main script is `PDF Tracking Program Grok.py`.

## Big-picture architecture
- Single Python script: `PDF Tracking Program Grok.py` contains DB schema, PDF storage (BLOB), text extraction, search and retrieval helpers, and a demonstration `main()`.
- Persistence: local SQLite database file `pdf_database.db` created in the working directory. Table: `pdfs(id, name, data, extracted_text)`.
- PDF processing: uses PyMuPDF (`fitz`) to extract page text. PDFs are stored as raw BLOBs in the DB (intentional design choice).

## Key files / symbols to inspect
- `PDF Tracking Program Grok.py` — important functions: `init_db()`, `store_pdf(cursor, conn, pdf_path)`, `extract_text_from_pdf(pdf_path)`, `search_pdfs(cursor, query, search_type='name')`, `retrieve_pdf(cursor, conn, pdf_id, output_path)`, and the `main()` demo.

## Developer workflows (concrete commands — PowerShell)
- Create a venv and install deps:
  ```powershell
  python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install pymupdf
  ```
- Run the script from repository root:
  ```powershell
  python "PDF Tracking Program Grok.py"
  ```
- Notes: the script writes `pdf_database.db` to the current working directory. In `main()` change `pdf_directory` and `output_directory` placeholders to real paths before running.

## Project-specific conventions and patterns
- Single-file editing: there is no package layout or CLI — changes are made directly in the script.
- Error handling: functions generally print errors and return defaults (e.g., `extract_text_from_pdf` returns empty string on failure). Avoid converting prints to exceptions unless testing/consuming code is updated accordingly.
- Storage format: PDFs are intentionally stored as BLOBs in SQLite. Do not change this storage format without an explicit migration plan from the repo owner.

## Integration points & dependencies
- PyMuPDF (imported as `fitz`) — used for text extraction. Install via `pip install pymupdf`.
- SQLite (`sqlite3` from stdlib) — DB file `pdf_database.db` (local file). No network services.

## Typical agent tasks (concrete, repo-relevant)
- Add a small CLI: modify `main()` to accept arguments (e.g., argparse) and replace hardcoded `pdf_directory`/`output_directory` with flags.
- Add tests: create `tests/test_core.py` that uses `tempfile` or pytest `tmp_path` to create a temporary DB file, call `init_db()` with a custom path (or patch `sqlite3.connect`) and assert `store_pdf`, `search_pdfs`, and `retrieve_pdf` behavior using a tiny fixture PDF.
- Harden extraction: handle encrypted PDFs (check `doc.is_encrypted`) and skip/record failures; process large PDFs page-by-page to avoid excessive memory use.

## Small, safe refactors you can do now
- Move the CREATE TABLE SQL into a small helper or constant to make schema changes easier.
- Add a lightweight logger (Python `logging`) but keep default behavior similar to current prints unless the owner requests changing CLI output.

## Red flags / do not change without confirmation
- Do NOT change the storage format (BLOBs -> file-based) without an explicit migration plan and confirmation.
- Avoid adding network or cloud storage; this project is intentionally local-first.

## Quick references (examples in repo)
- DB file: `sqlite3.connect('pdf_database.db')` — relative to the working directory.
- Example search usage in `main()`: `search_pdfs(cursor, 'example', search_type='name')` or `search_pdfs(cursor, 'Python', search_type='text')`.

---
If anything above is unclear or you'd like a follow-up (add CLI, tests, or convert prints to logging), tell me which item to implement next and I will update the repo accordingly.
