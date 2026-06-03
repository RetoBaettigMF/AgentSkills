# gog-db — Reference

Full spec for the `gog-db` skill. See `SKILL.md` for a quick tour.

## Storage layout

One Google Spreadsheet = one database. Inside the spreadsheet:

- `_schema` — the catalog tab. Always 7 columns:

  | table | column | type | pk | fk_table | fk_column | not_null |
  |-------|--------|------|----|----------|-----------|----------|

- `<table>` tabs — one per user table. Row 1 = header, row 2+ = data.
  Header order in the tab MUST match the order of columns in `_schema` for
  that table (the script writes both together; do not reorder columns by hand).

The spreadsheet ID lives in `~/.config/gog-db/config.json`:
```json
{ "active_db": "1AbCdEf...xyz" }
```

## Type system

| type       | example storage | Python type            |
|------------|-----------------|------------------------|
| `int`      | `42`            | `int`                  |
| `float`    | `3.14`          | `float`                |
| `str`      | `Alice`         | `str`                  |
| `bool`     | `true` / `false`| `bool`                 |
| `date`     | `2026-06-03`    | `datetime.date`        |
| `datetime` | `2026-06-03T14:30:00` | `datetime.datetime` |

- Empty cell = NULL (Python `None`).
- `not_null` columns reject NULL on insert/update.
- Bool inputs from the CLI accept `1/0`, `true/false`, `yes/no`, `y/n`, `t/f`.
- Dates/datetimes are stored as ISO strings; the script roundtrips through `date.fromisoformat`.
- Casting failures emit a clear error and exit non-zero.

## Column spec mini-grammar

`<name>:<type>[:pk][:not_null]`

- `name` — free text, but match what's safe for a sheet header (avoid commas).
- `type` — one of `int float str bool date datetime`.
- `pk` — exactly one column per table must be `:pk`. Implies `not_null`.
- `not_null` — also valid as `notnull`.

Multiple specs are comma-separated in `--columns`.

## Foreign keys

```
--fk "<col>:<target_table>.<target_col>"
```

- `--fk` repeats. Each call may itself contain a comma-separated list.
- Target table must already exist when `create-table` runs.
- Target column must be the PK of the target table.
- Types must match exactly between FK column and PK column.

### Strict enforcement (write-time)

- `insert`: for every FK column whose value is non-NULL, the script reads the
  target table and verifies the value exists in the target PK column. Missing
  match → exit code 2.
- `update`: same check, but only for FK columns that appear in `--set`.
- `delete`: for every FK that points at the deleted table, the script reads
  the referencing table and verifies no row points at any deleted PK. If any
  do, the delete is refused (exit 2). There is no cascade — delete the
  referencing rows yourself first.
- `drop-table`: refused if any FK in `_schema` still points at this table.
  `--force` overrides (leaves dangling FK definitions in `_schema`; run
  `check` afterwards).

### Lazy verification

`gog-db check` re-scans every FK against the current data and exits with code 2 if any orphans exist, printing them. Useful after manual edits or `--force` drops.

## WHERE grammar

```
<col><op><value>[,<col><op><value>...]
```

- Clauses are joined with implicit AND.
- Operators (longest match wins): `<=`, `>=`, `!=`, `=`, `<`, `>`, ` like `.
- `like` uses `%` (any chars) and `_` (one char), case-insensitive.
- Values are cast using the target column's type — `where age=30` works on an
  `int` column without quoting.
- Commas inside values are not supported (they're the clause separator). Same
  for `=` inside `--set` values.
- There is no OR. Compose with multiple selects + script logic if needed.
- There is no join. FKs document relations; cross-table reasoning is done by
  the caller (chained selects, often on PK).

## --set grammar

```
<col>=<value>[,<col>=<value>...]
```

Same comma/equals limitations as WHERE.

## Output

| Mode                       | When         | Format             |
|----------------------------|--------------|--------------------|
| Pretty table               | default      | aligned, stdout    |
| JSON                       | `--json` flag (before subcommand, e.g. `gog-db --json select ...`) | one JSON value, stdout |
| Errors                     | always       | stderr             |

`insert`'s `--json` flag is the row payload (string value), not the output mode.
Use the parent flag `gog-db --json insert ...` to get JSON-formatted confirmation.

## Exit codes

| Code | Meaning                                          |
|------|--------------------------------------------------|
| 0    | success                                          |
| 1    | usage / parse / I/O error                        |
| 2    | constraint violation: duplicate PK, FK violation, referenced row blocking delete, dangling FK found by `check` |

## `gog` commands used

| Operation         | `gog` call                                                    |
|-------------------|---------------------------------------------------------------|
| Create DB         | `gog sheets create <title> [--parent <folder>]`               |
| Spreadsheet info  | `gog sheets metadata <id>`                                    |
| Add tab           | `gog sheets add-tab <id> <name>`                              |
| Delete tab        | `gog sheets delete-tab <id> <name> --force`                   |
| Read range        | `gog sheets get <id> <a1> --render UNFORMATTED_VALUE`         |
| Overwrite range   | `gog sheets update <id> <a1> --values-json <2D> --input RAW`  |
| Append rows       | `gog sheets append <id> <range> --values-json <2D> --input RAW --insert INSERT_ROWS` |
| Clear range       | `gog sheets clear <id> <range>`                               |

All calls use `--json` for parsable output and pass arguments as a Python list
to `subprocess.run` — never as a shell string. This sidesteps the
quoting/`&`/long-body issues documented in the `gogcli` skill's `gmail-pitfalls.md`.

## Concurrency

There is no locking. Two parallel `gog-db` calls writing the same table will
race: the last `update`/`delete` (which does a full rewrite of rows 2+) wins,
silently overwriting the other's changes. For single-user / single-agent usage
this is fine; for shared write paths, serialise externally.

## Rate limiting

Google Sheets API limit: **60 read requests per minute per user**. The script
self-throttles to stay under a configurable cap and retries on HTTP 429.

### Configuration

Stored in `~/.config/gog-db/config.json` alongside `active_db`:

| Key                         | Default | Meaning                                                      |
|-----------------------------|---------|--------------------------------------------------------------|
| `max_requests_per_minute`   | `60`    | Max `gog` invocations per 60-second sliding window           |
| `max_retries`               | `3`     | Retry attempts when `gog` returns 429 / `rateLimitExceeded`  |

Set via:
```bash
scripts/gog-db config show
scripts/gog-db config set max-requests-per-minute 50
scripts/gog-db config set max-retries 5
```

Or edit the JSON file directly.

### How throttling works

A sliding window of issue-times is persisted to `~/.config/gog-db/rate.json`
(a JSON array of unix timestamps). Before each `gog` invocation the script:
1. Loads the window, drops entries older than 60s.
2. If `len(window) >= max_requests_per_minute`, sleeps until the oldest entry
   ages out (plus 0.1s headroom).
3. Records the new timestamp and proceeds.

This file is shared across processes — running two `gog-db` commands back-to-back
respects the same minute window. Concurrent writers race on the file; the last
writer wins, so the cap is approximate under heavy parallelism (the retry path
catches any overshoot).

### How retry works

`subprocess.run` captures stderr. If `gog` returns non-zero AND stderr contains
`rateLimitExceeded` / `Quota exceeded` / a 429 marker, the script:
1. Logs the wait to stderr.
2. Sleeps `RATE_WINDOW_SECONDS + ~1s` (force-clears the window).
3. Retries, up to `max_retries` times.

Non-rate-limit failures (auth, parse errors, etc.) are not retried — they exit
immediately with the original exit code.

### Caveats

- The cap counts `gog` invocations, not `gog-db` commands. A single `select`
  typically issues 2-3 `gog` calls (schema + table + FK checks). Plan your cap
  accordingly: if you want ~30 `gog-db` commands per minute, leave the cap at 60.
- Google's "write requests per minute per user" is a separate 60 quota. The
  script's single cap covers both, so heavy write loops are slightly over-throttled
  on read but never under-throttled on write.
- A bug or stale clock can leave bogus timestamps in `rate.json`. Safe to delete
  if you suspect drift: `rm ~/.config/gog-db/rate.json`.
- Manual edits in the Sheets UI are allowed for **values**. Do **not** reorder
  the header row or rename columns — the script trusts the column order in
  `_schema` to map row positions back to names.
- A very large table makes update/delete slow: the implementation
  reads-then-rewrites all data rows. Inserts are O(1) (`sheets append`).
- `like` regex is built by replacing `%`/`_` and escaping the rest. Very long
  patterns or pathological values are not adversarial-safe; this is a private
  data tool, not a public API.
- Bool storage format is `true`/`false` strings, not the Sheets boolean cell
  type. Filter formulas in the Sheets UI need to compare against strings.
