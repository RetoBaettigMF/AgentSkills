---
name: crm
description: Abfrage von Kontakten, Firmen, Verkaufschancen und Kommentaren aus berliCRM via REST API. Verwende diesen Skill bei Fragen über CRM-Daten, Kundendaten, Accounts, Kontakte, Potentials, Kommentare oder direkte SQL-Abfragen gegen das CRM.
---

# CRM Skill

Zugriff auf berliCRM via REST API mit JSON-Output. Unterstützt Suche, Detailabfragen und direkte SQL-ähnliche Queries.

**Vollständiges Schema, alle Felder und Auswahlwerte: `CRM_SCHEMA.md`**

## Voraussetzungen

Zugangsdaten müssen in `scripts/.env` gesetzt sein (siehe `.env.example`):

```
CRM_URL=https://crm.example.com
CRM_USER=username
CRM_API_KEY=your_api_key
```

## Verwendung

```bash
scripts/crm <subcommand> [argument]
```

Verwende nur folgende subcommands:
- search-comments
- details
- query

Versuche, die Menge von Rückgabedaten zu begrenzen, um die Übersicht zu behalten (z.B. durch WHERE-Bedingungen oder LIMIT in SQL-Queries). Alle Ergebnisse werden als JSON ausgegeben, Fehler auf stderr.
Mache auch nicht "select *" für lange Listen, sondern wähle nur die benötigten Spalten aus (z.B. "select accountname, email from Contacts where ...").

## Befehle

### Kommentare einer Firma abrufen
```bash
scripts/crm account-comments "Cudos AG"
scripts/crm account-comments 3x12345     # direkt per CRM-ID
```

### Objekt-Details per ID
```bash
scripts/crm details 4x2712    # Kontakt
scripts/crm details 3x12345   # Firma/Account
scripts/crm details 13x456    # anderes Objekt
```

### Direkte SQL-ähnliche Abfrage
```bash
scripts/crm query "select * from Contacts where email like '%cudos%' limit 0, 20;"
scripts/crm query "select * from Accounts where accountname = 'Cudos AG' limit 0, 5;"
```

## CRM-ID Format

CRM-Objekt-IDs haben das Format `<TypeId>x<ObjectId>`:
- `4x2712` → Kontakt
- `3x12345` → Firma/Account
- `5x456` → Potential/Verkaufschance
- `29x789` → Kommentar

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

---

## Wichtige Felder (Kurzreferenz)

### Accounts – meistgenutzte Felder
- `accountname` – Firmenname (Suchfeld)
- `industry` – Branche (z.B. `Maschinenbau`, `Elektronik`, `Medizin`)
- `accounttype` – `Kunde`, `Freelancer`, `Lieferant`, `Mitbewerber`, `andere`
- `cf_654` – Kundeninteresse: `1 - Kunde`, `2 - ex Kunde`, `3 - Potentieller Kunde`, `4 - Kein Interesse`
- `cf_615` / `cf_632` / `cf_940` – Potential (SW-Eng / AI / Prüfsystem): `1 - High Potential` bis `4 - Kein Potential`
- `cf_669` – Entscheider/Geschäftsführer (Namen)
- `cf_671` – Firmenbeschreibung

### Contacts – meistgenutzte Felder
- `firstname`, `lastname`, `email`, `phone`
- `account_id_nameValue` – Firmenname (automatisch)
- `cf_546` – Abteilung/Funktion (Freitext)
- `cf_576` – Kontakttyp: `Engineering Interessent`, `Engineering Beeinflusser`, `CT Beeinflusser`
- `cf_605` – Newsletter: `Ja` / `Nein`
- `cf_555` – Sprache: `Deutsch`, `Englisch`, `Französisch`

### Potentials – meistgenutzte Felder
- `potentialname` – Bezeichnung, oft `Firma: Projektname`
- `sales_stage` – **Leer = aktiv!** Sonst: `Closed Won`, `Closed Lost`, `gestorben`, `inaktiv`
- `amount` – Auftragswert (CHF)
- `cf_587` – Kategorie: `Software Engineering`, `AI (Künstliche Intelligenz)`, `Prüfsystem`, `IIoT`, `Cudos Trail`
- `cf_659` – Aufwand geschätzt (CHF)
- `cf_958` / `cf_960` – Letzter / nächster Kontakt (Datum)
- `related_to_nameValue` – Firmenname (automatisch)

### ModComments – meistgenutzte Felder
- `commentcontent` – Kommentartext (Suchfeld)
- `related_to` – Verknüpfte Objekt-ID
- `related_to_nameValue` – Name des Objekts (automatisch)
- `createdtime` – Datum des Kommentars

---

## Fuzzy-Suche nach Firmennamen

Firmennamen variieren oft (`Walo Bertschinger AG` vs. `Walo Bertschinger Central AG`):

```bash
# Schlüsselwort reicht meist
scripts/crm query "select id, accountname from Accounts where accountname like '%Bertschinger%' limit 0, 10;"

# Mehrere Keywords kombinieren
scripts/crm query "select id, accountname from Accounts where accountname like '%Walo%' and accountname like '%Bertschinger%' limit 0, 10;"
```

**Regeln:**
1. Firmentyp-Suffix weglassen (AG, GmbH, SA, Ltd.) – er variiert zu oft
2. Den markantesten Namensteil nutzen
3. Bei mehreren Treffern: ID erfragen, dann mit `3xNNN` weiterarbeiten
4. Multi-Select Felder (`cf_956`, `cf_575`, `cf_576`) immer mit `like` statt `=` filtern

---

## Typische Abfragen

```bash
# Aktive Verkaufschancen (sales_stage leer = offen)
scripts/crm query "select potentialname, amount, closingdate, related_to_nameValue from Potentials where sales_stage = '' order by closingdate limit 0, 50;"

# High-Potential Firmen SW-Engineering
scripts/crm query "select accountname, industry, phone, email1 from Accounts where cf_615 = '1 - High Potential' limit 0, 50;"

# Fällige Follow-ups
scripts/crm query "select potentialname, cf_960, related_to_nameValue from Potentials where sales_stage = '' and cf_960 <= '2026-04-25' order by cf_960 limit 0, 30;"

# Kontakte einer Firma
scripts/crm query "select firstname, lastname, title, email, cf_546 from Contacts where account_id = '3x12345' limit 0, 20;"
```
