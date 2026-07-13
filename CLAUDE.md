# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

sqlite_bro is a graphic SQLite browser/client implemented as a **single Python source file**:
`sqlite_bro/sqlite_bro.py` (~2300 lines). Keeping the tool in one file is a deliberate design goal
(see README.rst: "Easy to distribute : 1 Python source file") — it's meant to be copied to any
machine and run directly with `python sqlite_bro.py`, or loaded remotely via
`%load https://raw.githubusercontent.com/stonebig/sqlite_bro/master/sqlite_bro/sqlite_bro.py`.
Avoid splitting it into multiple modules.

Supports Python >= 3.3 and PyPy3. Uses Tkinter/ttk for the GUI (`from tkinter import *`, with a
Python 2.7 fallback import path still present via `from __future__ import ...`).

## Common commands

Install in editable mode and run:
```
pip install -e .
sqlite_bro            # launch the GUI
sqlite_bro -h          # see CLI options (-q/--quiet, -w/--wait, -db/--database, -sc/--scripts)
python -m sqlite_bro.sqlite_bro   # run directly without install
```

Run tests (from repo root):
```
pytest -v
pytest -v sqlite_bro/tests/test_general.py::test_Basics   # single test
```

- `test_general.py` drives the real Tkinter GUI app (`App()`); on Linux CI this needs a virtual
  display (Xvfb) since there's no `DISPLAY` otherwise.
- `test_general_no_gui.py` is the same test suite against `App(use_gui=False)`, exercising the
  command/query engine without Tkinter widgets.

Lint (as run in CI, see `.github/workflows/tests.yml`):
```
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

CI matrix: Python 3.8, 3.12, and pypy-3.10 (`.github/workflows/tests.yml`). `appveyor.yml` is legacy
(Python 2.7/3.4, nosetests) and not the active CI.

Build/publish uses `flit_core` (see `pyproject.toml`), not setuptools — version is read from
`sqlite_bro/__init__.py`'s `__version__`.

## Architecture

Everything lives in `sqlite_bro/sqlite_bro.py`. The major pieces, in order of appearance:

- **`App`** — the Tkinter application. Can run with or without a GUI (`use_gui` flag), which is
  what lets the query/script engine be tested headlessly. Owns the DB connection lifecycle
  (`new_db`, `open_db`, `backup_db`, `restore_db`, `attach_db`, `close_db`), the menu/toolbar, the
  font/tab UI (drag-reorder tabs via `btn_press`/`btn_Move`/`btn_release`), CSV import/export
  dialogs, and the DB-tree view (`feed_dbtree`).
- **`App.create_and_add_results`** — the core script execution engine (the largest method, ~1000
  lines). It splits a multi-statement script into individual instructions via
  `Baresql.get_sqlsplit`, then for each instruction dispatches on its shape:
  - `pydef ...` blocks → registers an embedded Python function as a SQLite function
    (`Baresql.createpydef`), so SQL can call user-defined Python (see the `.` command doc block in
    `_main()`'s `welcome_text` and the `py_hello`/`py_fib` examples).
  - `.` prefixed lines → **dot-commands** (sqlite3-CLI-style), parsed with `shlex.split`. Supported:
    `.backup`, `.cd`, `.dump`, `.excel`, `.headers`, `.import`, `.once`, `.open`, `.output`,
    `.print`, `.read`, `.restore`, `.separator`, `.shell`. This is what gives sqlite_bro its
    command-line scripting story independent of the GUI.
  - everything else → run as SQL against `Baresql.conn`, with results rendered into the tab's
    treeview (`NotebookForQueries.add_treeview`).
- **`NotebookForQueries`** — manages the query-tab notebook: creating tabs (`new_query_tab`),
  attaching result treeviews to a tab, and sortable columns (`sortby`).
- **`Baresql`** — thin wrapper around `sqlite3.Connection`. Handles: dump export tweaks
  (`iterdump`, forces a UTF-8 marker, toggles `PRAGMA foreign_keys` around dumps), SQL tokenizing
  and statement splitting (`get_tokens`, `get_sqlsplit` — this is what makes multi-statement
  scripts and dot-commands work inside one text blob), and CSV import/export row streaming
  (`insert_reader`, `export_writer`).
- **`guess_csv`** / **`guess_encoding`** / **`guess_sql_creation`** — CSV format and file-encoding
  auto-detection used by import/export, independent of `Baresql`.
- **`create_dialog`** — generic Tkinter modal-dialog builder reused by several features (rename
  tab, import CSV, export CSV, etc.) rather than each having bespoke dialog code.
- **`_main()`** — CLI entry point (`sqlite_bro = "sqlite_bro.sqlite_bro:_main"` in
  `pyproject.toml`). Builds the built-in "Welcome" demo script (which doubles as living
  documentation of SQL features and dot-commands), parses argv with `argparse` (falls back to no
  CLI args pre-3.2), and boots `App`.

When editing, keep in mind the GUI/no-GUI duality: any change to script/command execution
(`create_and_add_results`, `Baresql`) must keep working under `use_gui=False`, since that's the
path exercised by `test_general_no_gui.py` and by headless/CLI usage (`-q/--quiet`).
