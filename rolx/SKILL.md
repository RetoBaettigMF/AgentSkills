---
name: rolx
description: Kann detaillierte Infos zu Stundenerfassung und Projekt-Zeiterfassung aller Cudos-Mitarbeitenden abfragen (RolX Integration). Verwende dieses Tool bei Fragen über Projektstunden, Zeiterfassungsdaten, Arbeitsstunden oder Anfragen zu "RolX"
---

# RolX Skill

Zeiterfassung und Projektstunden für Cudos AG via das RolX Modul des CudosControlling Tools.

## Voraussetzungen

API key muss in `./scripts/.env` als `MBTOOLS_API_KEY` gesetzt sein (siehe `.env.example`).

## Verwendung

### Stunden abfragen

```bash
scripts/cudos_controlling.py rolx "<Natürlichsprachige Anfrage>"
```

**Projektnummern-Format:**
- `#0123.002` oder `0123.002` → Projekt 123, Subprojekt 2
- Wird automatisch erkannt und geparst

## Beispiele

### Mitarbeiter-Stunden
```bash
scripts/cudos_controlling.py rolx "Wie viele Stunden hat Reto gearbeitet in Januar 2025?"
```

### Projektbasierte Abfragen
```bash
scripts/cudos_controlling.py rolx "Show all hours for project 0123.110"
scripts/cudos_controlling.py rolx "Gib mir alle Stunden für Projekt #0123.002 im Februar 2026"
scripts/cudos_controlling.py rolx "Zeige alle Stunden pro Aufgabe für Projekt 0123.002 im Januar 2026"
```

