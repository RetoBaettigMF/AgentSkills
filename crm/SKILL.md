---
name: crm
description: Abfrage von Kontakten, Firmen, Verkaufschancen und Kommentaren aus berliCRM via REST API. Verwende diesen Skill bei Fragen über CRM-Daten, Kundendaten, Accounts, Kontakte, Potentials, Kommentare oder direkte SQL-Abfragen gegen das CRM.
---

# CRM Skill

Zugriff auf berliCRM via REST API mit JSON-Output. Unterstützt Suche, Detailabfragen und direkte SQL-ähnliche Queries.

## Voraussetzungen

Zugangsdaten müssen in `scripts/.env` gesetzt sein (siehe `.env.example`):

```
CRM_URL=https://crm.example.com
CRM_USER=username
CRM_API_KEY=your_api_key
```

## Verwendung

```bash
scripts/crm.py <subcommand> [argument]
```

## Befehle

### Kontakte suchen
```bash
scripts/crm.py search-contacts "Max Muster"
scripts/crm.py search-contacts "max@example.com"
```

### Firmen/Accounts suchen
```bash
scripts/crm.py search-accounts "Cudos AG"
scripts/crm.py search-accounts "cudos"
```

### Verkaufschancen suchen
```bash
scripts/crm.py search-potentials "Cloud Migration"
```

### Kommentare suchen
```bash
scripts/crm.py search-comments "onboarding"
scripts/crm.py search-comments "meeting"
```

### Kommentare einer Firma abrufen
```bash
scripts/crm.py account-comments "Cudos AG"
scripts/crm.py account-comments 3x12345     # direkt per CRM-ID
```

### Objekt-Details per ID
```bash
scripts/crm.py details 4x2712    # Kontakt
scripts/crm.py details 3x12345   # Firma/Account
scripts/crm.py details 13x456    # anderes Objekt
```

### Direkte SQL-ähnliche Abfrage
```bash
scripts/crm.py query "select * from Contacts where email like '%cudos%' limit 0, 20;"
scripts/crm.py query "select * from Accounts where accountname = 'Cudos AG' limit 0, 5;"
```

## CRM-ID Format

CRM-Objekt-IDs haben das Format `<TypeId>x<ObjectId>`:
- `4x2712` → Kontakt
- `3x12345` → Firma/Account
- `13x456` → anderes Objekt

## SQL-Query Syntax

```sql
select * | <spalten> | count(*)
from <Modul>
[where <bedingungen>]
[order by <spalten>]
[limit [<offset>,] <anzahl>];
```

**Module:** `Contacts`, `Accounts`, `Potentials`, `ModComments`  
**Operatoren:** `<`, `>`, `<=`, `>=`, `=`, `!=`, `like`, `in()`  
**Limit:** Max. 100 Datensätze pro Abfrage (Offset für Paginierung nutzen)

## Output

Alle Ergebnisse werden als JSON auf stdout ausgegeben. Fehler gehen auf stderr.
