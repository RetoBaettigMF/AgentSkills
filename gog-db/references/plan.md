# Plan: `gog-db` skill — DB-like interface over Google Sheets

## Context

We want a new AgentSkill that lets agents (and humans) treat Google Sheets as a small relational database: create tables, insert/update/delete/select rows, declare primary keys and foreign keys, and run simple queries. Storage is one Google Spreadsheet per database (tabs = tables). All Sheets API calls go through the already-installed `gog` CLI (`gogcli`), so we don't reinvent auth.

Why this is useful: lightweight shared state for agents (CRM-lite, task trackers, lookup tables) without standing up a real DB, and the data stays human-editable in Sheets.

User decisions (already gathered):
- **Layout:** one spreadsheet per DB, one tab per table, plus a `_schema` tab as catalog.
- **CLI style:** subcommand + flags (no SQL parser).
- **FK enforcement:** strict on write — every insert/update verifies referenced rows exist; deletes blocked if referenced.

## Skill layout

```
/Users/morticiamac/.hermes/skills/AgentSkills/gog-db/
├── SKILL.md                  # frontmatter + usage docs
├── scripts/
│   └── gog-db                # uv-run python CLI (PEP 723 inline deps)
└── references/
    └── REFERENCE.md          # schema format, type system, edge cases
```

Conventions match `crm/` and `bexio/`:
- Script has shebang `#!/usr/bin/env -S uv run --script` with inline `# /// script` deps.
- Invoked from SKILL.md as `scripts/gog-db <subcommand> ...` (no `python3`/`uv` prefix).
- No `pyproject.toml`.

## Storage model

One Google Spreadsheet = one database. Tabs:

- `_schema` — catalog. Columns:
  - `table` — table name (= tab name in the same spreadsheet)
  - `column` — column name
  - `type` — `int` | `float` | `str` | `bool` | `date` (ISO `YYYY-MM-DD`) | `datetime` (ISO 8601)
  - `pk` — `1` if primary-key column, else blank
  - `fk_table` — referenced table (blank if none)
  - `fk_column` — referenced column (blank if none)
  - `not_null` — `1` if required, else blank
- `<table>` tabs — first row is the header (column names matching `_schema`), data starts at row 2.

Rules:
- Exactly one PK column per table (auto-checked at `create-table`).
- FK column type must equal the referenced PK type.
- Reserved names: any tab starting with `_` (only `_schema` is used today; leaves room for `_meta`, `_seq` later).

## CLI surface

```
gog-db init <spreadsheet-title> [--parent <driveFolderId>]   # create new DB spreadsheet
gog-db use <spreadsheetId>                                   # remember active DB (local config)
gog-db list-tables
gog-db create-table <table> --columns "id:int:pk,name:str:not_null,account_id:int" \
                            --fk "account_id:accounts.id"
gog-db drop-table <table>
gog-db describe <table>

gog-db insert <table> --json '{"id":1,"name":"Bob","account_id":7}'
gog-db update <table> --where "id=1" --set "name=Foo,account_id=8"
gog-db delete <table> --where "id=1"
gog-db select <table> [--where "col<op>val[,col<op>val...]"] [--columns "a,b"] \
                      [--order-by "col[:desc]"] [--limit N] [--json]

gog-db check                                                 # verify all FKs across DB
```

Notes:
- `--where` supports comma-separated AND-only clauses with ops `=`, `!=`, `<`, `<=`, `>`, `>=`, `like` (e.g. `name like %foo%`). That's the agreed "simple queries" scope — no OR, no joins on the CLI surface (foreign keys help readers compose by hand).
- All commands accept `--db <spreadsheetId>` to override the active DB; otherwise fall back to local config.

## Local config

`~/.config/gog-db/config.json`:
```json
{ "active_db": "<spreadsheetId>" }
```
Set by `gog-db use`. Read by every other command. Per-skill convention is fine since `crm` already uses `scripts/.env`; we use `~/.config/...` because the DB ID is user-state, not skill-state.

## Implementation outline (`scripts/gog-db`)

PEP 723 deps: stdlib only is enough (`argparse`, `json`, `subprocess`, `pathlib`, `csv`, `re`, `datetime`). No `python-dotenv` needed — config is JSON.

Core helpers:
- `gog_json(*args) -> dict` — runs `gog --json <args>`, parses stdout, raises on non-zero exit (passes stderr through).
- `read_tab(db, tab) -> list[dict]` — `gog sheets get <db> '<tab>'!A:ZZ --json`, first row = headers, rest = rows; cast per `_schema`.
- `write_tab_rows(db, tab, rows)` — used by `update`/`delete`: rewrite affected rows with `gog sheets update`. For `insert`: `gog sheets append`.
- `load_schema(db)` — read `_schema` tab once per invocation, return `{table: {pk, columns: {name: ColumnSpec}, fks: [...]}}`.
- `parse_where(expr)` → list of `(col, op, value)` predicates.
- `eval_predicates(row, predicates)` — bool filter.
- `cast(value, type)` / `format(value, type)` — string ↔ typed roundtrip; dates stay ISO.

Subcommand wiring (argparse subparsers): `init`, `use`, `list_tables`, `create_table`, `drop_table`, `describe`, `insert`, `update`, `delete`, `select`, `check`.

FK strictness path:
- `insert`: for each FK column with a non-empty value, run `select` against the referenced table and verify exactly one row matches; reject otherwise.
- `update`: same check when an FK column is in `--set`.
- `delete`: for each table that references this one (look up via `_schema`), run `select` on the referencing column for the deleted PK value; refuse if any match. No cascade in v1 — explicit.
- `check`: full scan, report orphans to stderr, exit non-zero if any.

Shell-quoting safety: always pass arguments to `gog` as a Python list to `subprocess.run` (no `shell=True`), matching the gmail-pitfalls.md guidance. Range strings like `users!A1:Z` are single args, never f-string-interpolated into a shell command.

## Files to create

1. `/Users/morticiamac/.hermes/skills/AgentSkills/gog-db/SKILL.md`
   - Frontmatter: `name: gog-db`, `description:` includes triggers like "google sheets database", "table in sheets", "store structured data", "simple query in sheets".
   - Sections: Voraussetzungen (`gog` installed + authed), Verwendung, Befehlsreferenz (the CLI surface above), Schema-Format, Pitfalls, Beispiele (create + insert + select + FK violation).
2. `/Users/morticiamac/.hermes/skills/AgentSkills/gog-db/scripts/gog-db` (executable `chmod +x`).
3. `/Users/morticiamac/.hermes/skills/AgentSkills/gog-db/references/REFERENCE.md` — detailed `_schema` tab format, type-casting rules, the full `--where` grammar, FK behavior, exit codes.

## Reused / referenced existing code

- Script shape modeled on `crm/scripts/crm` (argparse + subprocess + JSON to stdout, errors to stderr).
- `gog` commands used (verified live via `gog sheets --help` / `gog drive --help`):
  - `gog sheets create <title> [--parent <folderId>] [--sheets <names>] --json` — initial DB + `_schema` tab.
  - `gog sheets add-tab <id> <name>` — create-table.
  - `gog sheets get <id> '<tab>!A:ZZ' --json` — read.
  - `gog sheets update <id> '<tab>!A2' --values-json '[[...]]'` — overwrite rows.
  - `gog sheets append <id> '<tab>!A:Z' --values-json '[[...]]'` — insert.
  - `gog sheets clear <id> '<tab>!A2:Z'` — bulk delete with rewrite-after.
- Pitfalls: long arg lists / quoting — pass as subprocess list, never shell string (`references/gmail-pitfalls.md`).

## Verification

End-to-end smoke test (run after implementation):
```bash
cd /Users/morticiamac/.hermes/skills/AgentSkills/gog-db
scripts/gog-db init "gogdb-smoke-$(date +%s)"          # prints spreadsheetId
scripts/gog-db use <id>
scripts/gog-db create-table accounts --columns "id:int:pk,name:str:not_null"
scripts/gog-db create-table users    --columns "id:int:pk,name:str,account_id:int" \
                                     --fk "account_id:accounts.id"
scripts/gog-db insert accounts --json '{"id":1,"name":"Cudos"}'
scripts/gog-db insert users    --json '{"id":1,"name":"Reto","account_id":1}'
scripts/gog-db insert users    --json '{"id":2,"name":"Orphan","account_id":99}'   # MUST fail (FK)
scripts/gog-db select users --where "account_id=1" --json                          # 1 row
scripts/gog-db update users --where "id=1" --set "name=Reto B."
scripts/gog-db delete accounts --where "id=1"                                       # MUST fail (referenced)
scripts/gog-db check                                                                 # exit 0
scripts/gog-db list-tables
```
Open the spreadsheet in the browser at the end to eyeball the `_schema` and data tabs.

Cleanup: leave the smoke spreadsheet in place (cheap, useful for re-running) or delete via `gog drive` if the user prefers a clean Drive.
