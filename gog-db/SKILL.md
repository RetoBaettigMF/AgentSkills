---
name: gog-db
description: Use Google Sheets as a small relational database. Create tables, insert/update/delete/select rows, declare primary keys and foreign keys, run simple WHERE queries. Backed by gogcli (`gog`). Trigger on "Tabelle in Google Sheets", "Daten als Tabelle speichern", "kleine Datenbank", "Sheets als Datenbank", "google sheets database", "store structured data in sheets".
---

# gog-db — DB-like CLI over Google Sheets

Treat one Google Spreadsheet as a tiny relational database. Tabs are tables, the
`_schema` tab is the catalog, primary keys and foreign keys are enforced on
writes. All API calls go through `gog` (gogcli), so authentication is whatever
`gog` is already using.

## Voraussetzungen

- `gog` ist installiert und authentifiziert (siehe Skill `gogcli`).
- Script wird direkt ausgeführt (kein `python3`, kein `uv` davor):
  ```bash
  scripts/gog-db <subcommand> [...]
  ```

## Datenmodell

- **1 Spreadsheet = 1 Datenbank** (lebt irgendwo in Drive, in einem beliebigen Ordner).
- **1 Tab = 1 Tabelle**. Erste Zeile = Header, Datenzeilen ab Zeile 2.
- **`_schema` Tab** (automatisch angelegt) = Katalog mit Spalten:
  `table | column | type | pk | fk_table | fk_column | not_null`
- Typen: `int`, `float`, `str`, `bool`, `date` (ISO `YYYY-MM-DD`), `datetime` (ISO 8601).
- Genau eine PK-Spalte pro Tabelle. FK-Spaltentyp muss zum Ziel-PK passen.
- Tabnamen mit `_` Präfix sind reserviert.

Vollständige Spezifikation: `references/REFERENCE.md`.

## Aktive Datenbank

`gog-db use <id>` merkt sich die Spreadsheet-ID in `~/.config/gog-db/config.json`.
Alle weiteren Befehle nutzen diese DB. Einzelne Aufrufe können mit
`--db <id>` überschrieben werden.

## Rate-Limiting

Google Sheets erlaubt 60 Read-Requests pro Minute pro User. Das Skript
throttled automatisch (gleitendes Fenster, persistiert in
`~/.config/gog-db/rate.json` — funktioniert über Prozessgrenzen hinweg) und
versucht es bei einem 429 nach einer Wartezeit erneut.

```bash
scripts/gog-db config show
scripts/gog-db config set max-requests-per-minute 50   # Headroom unter dem 60er-Limit
scripts/gog-db config set max-retries 5
```

Hinweis: Ein einzelner `gog-db`-Befehl kann mehrere `gog`-Calls auslösen
(z.B. `select` = Schema lesen + Tabelle lesen + ggf. FK-Targets). Der Cap
gilt für `gog`-Calls, nicht für `gog-db`-Befehle.

## Befehle

### Datenbank anlegen / wählen

```bash
scripts/gog-db init "Meine DB" [--parent <driveFolderId>]   # erzeugt neue DB, setzt als aktiv
scripts/gog-db use <spreadsheetId>                          # bestehende DB als aktiv setzen
```

### Tabellen verwalten

```bash
scripts/gog-db list-tables
scripts/gog-db describe <table>

scripts/gog-db create-table users \
  --columns "id:int:pk,name:str:not_null,email:str,age:int"

scripts/gog-db create-table orders \
  --columns "id:int:pk,user_id:int:not_null,total:float" \
  --fk "user_id:users.id"

scripts/gog-db drop-table users [--force]   # --force, falls von anderer Tabelle referenziert
```

Spalten-Spec: `name:type[:pk][:not_null]`. `:pk` impliziert `not_null`.

### Datenmanipulation

```bash
# Insert: Zeile als JSON-Objekt
scripts/gog-db insert users --json '{"id":1,"name":"Alice","email":"a@x.com","age":30}'

# Update: Predicate(s) + SET-Liste (beides komma-separiert, AND-only)
scripts/gog-db update users --where "id=1" --set "age=31,email=alice@x.com"

# Delete: WHERE Pflicht, ausser --all explizit gesetzt
scripts/gog-db delete users --where "age<18"
scripts/gog-db delete users --all                            # wirklich alle Zeilen
```

### Abfragen

```bash
scripts/gog-db select users
scripts/gog-db select users --where "age>=18,name like %Al%"
scripts/gog-db select users --columns "name,email" --order-by "age:desc" --limit 5
scripts/gog-db select users --where "id=1" --json
```

WHERE-Operatoren: `=`, `!=`, `<`, `<=`, `>`, `>=`, `like` (mit `%`/`_` Wildcards).
Klauseln sind komma-separiert und werden mit AND verknüpft. OR/JOIN gibt es nicht —
für komplexere Logik mehrere Selects kombinieren.

### Foreign-Key Check

```bash
scripts/gog-db check    # scannt alle FKs, exit 2 bei dangling references
```

### Config

```bash
scripts/gog-db config show
scripts/gog-db config set max-requests-per-minute 50
scripts/gog-db config set max-retries 5
scripts/gog-db config set active-db <spreadsheetId>     # gleichbedeutend mit `use`
```

## Output

- Default: lesbare Tabelle auf stdout, Fehler auf stderr.
- `--json` (vor dem Subcommand): JSON statt Tabelle, z.B. `scripts/gog-db --json select users`.

## FK-Verhalten (strict)

- **insert / update**: jeder gesetzte FK-Wert muss in der referenzierten PK-Spalte existieren — sonst Exit 2.
- **delete**: blockt, wenn referenzierende Zeilen vorhanden sind. Kein Cascade — explizit erst die referenzierenden Zeilen löschen.
- **drop-table**: blockt, wenn FK auf diese Tabelle zeigt. `--force` überschreibt (lässt verwaiste FKs im `_schema`, danach `check` aufrufen).

## Beispiele

```bash
# Frische DB
scripts/gog-db init "ProjektDB"

# Tabellen anlegen
scripts/gog-db create-table accounts --columns "id:int:pk,name:str:not_null"
scripts/gog-db create-table users    --columns "id:int:pk,name:str,account_id:int" \
                                     --fk "account_id:accounts.id"

# Daten einfügen
scripts/gog-db insert accounts --json '{"id":1,"name":"Cudos AG"}'
scripts/gog-db insert users    --json '{"id":1,"name":"Reto","account_id":1}'

# Verletzt FK -> Exit 2
scripts/gog-db insert users --json '{"id":2,"name":"Orphan","account_id":99}'

# Auswerten
scripts/gog-db select users --where "account_id=1"
scripts/gog-db --json select accounts --columns "name"
```

## Pitfalls

- Werte mit Kommas in `--where` oder `--set` sind nicht unterstützt (das Komma ist der Klausel-Separator). Für solche Daten via `--json` und PK arbeiten.
- `gog` selber kann bei sehr grossen `--values-json` Argumenten zicken — Skript hält Tabellen aktuell unbegrenzt, aber > ~10k Zeilen sollten zerlegt werden.
- Manuelle Edits in Sheets sind möglich, aber: keine Spalten verschieben, Reihenfolge der Header muss dem `_schema` entsprechen.
- Sheets verwendet das Anmelde-Account von `gog`. Für Multi-Account siehe `gog auth add`.
