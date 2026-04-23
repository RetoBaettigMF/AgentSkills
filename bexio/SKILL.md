---
name: bexio
description: Abfrage von Kundenrechnungen und Finanzdaten (Bexio Integration). Trigger / Verwende den Skill bei Abfragen über "Rechnung", "Zeige Rechnung", "Bexio", "bills"
---

# Bexio Skill

Kundenrechnungen und Finanzdaten für Cudos AG via das Bexio Modul des CudosControlling Tools.

## Verzeichnis

**Script:** `scripts/cudos_controlling.py`

Das Script verwendet `uv run` (kein venv nötig).

## Verwendung

### Rechnungen abfragen

```bash
scripts/cudos_controlling.py bexio "<Natürlichsprachige Anfrage>"
```

**Rechnungsnummern-Format:**
- `#0158.003.01.01` → Format: `#XXXX.YYY.ZZ.VV`
- `#XXXX.YYY` (Auftragsnummer) ist identisch mit der Projektnummer aus RolX

## Beispiele

### Einzelne Rechnung abfragen
```bash
scripts/cudos_controlling.py bexio "Zeige Rechnung #0290.001.01.01"
scripts/cudos_controlling.py bexio "Rechnung #3771"
scripts/cudos_controlling.py bexio "gib mir die Rechnung #0158.003.01.01"
```
