---
name: moneyhouse
description: Automatisiertes Auslesen von Firmeninformationen von moneyhouse.ch via Browser-Automatisierung. Verwende diesen Skill bei Anfragen nach Firmendetails, Handelsregisterinformationen, Mitarbeiterzahlen, Zeichnungsberechtigten, Rechtsformen oder anderen Firmendaten von Schweizer Unternehmen.
---

# Moneyhouse Skill

Automatisierte Extraktion von Firmeninformationen von moneyhouse.ch via Playwright. Nutzt ein LLM (OpenRouter) zur strukturierten Datenextraktion.

## Voraussetzungen

Zugangsdaten in `scripts/.env` (siehe `.env.example`):

```
MONEYHOUSE_EMAIL=user@example.com
MONEYHOUSE_PASSWORD=yourpassword
OPENROUTER_API_KEY=sk-or-...
```

## Verwendung

```bash
scripts/moneyhouse.py "<Firmenname>" [Optionen]
```

## Beispiele

```bash
# Grundlegende Suche (Browser sichtbar)
scripts/moneyhouse.py "Cudos AG"

# Headless-Modus (Browser im Hintergrund)
scripts/moneyhouse.py "Muster AG" --headless

# Ausgabe in eigene Datei
scripts/moneyhouse.py "Cudos AG" -o cudos.json
```

## Parameter

| Parameter | Beschreibung | Pflicht |
|-----------|--------------|---------|
| `search_term` | Firmenname (z.B. `"Cudos AG"`) | Ja |
| `--headless` | Browser unsichtbar ausführen | Nein |
| `-o, --output` | Ausgabedatei (Standard: `output.json`) | Nein |
| `--model` | OpenRouter-Modell (Standard: `google/gemini-2.0-flash-001`) | Nein |

## Output-Format

```json
{
  "search_term": "Cudos AG",
  "results_count": 1,
  "companies": [
    {
      "Firmenname": "Cudos AG",
      "Strasse": null,
      "Hausnummer": null,
      "Postleitzahl": 8104,
      "Ort": "Weiningen",
      "AnzahlMitarbeitende": 35,
      "Umsatz": null,
      "Zeichnungsberechtigte": [
        {"Vorname": "Rachel", "Name": "Blaser", "Funktion": "Zeichnungsberechtigt"}
      ],
      "Rechtsform": "Aktiengesellschaft",
      "MWSTNr": "CHE-100.618.212",
      "Branche": "Erbringen von IT-Dienstleistungen",
      "Firmenzweck": "Die Gesellschaft bezweckt ...",
      "ListeZweigniederlassungen": ["Cudos AG, Zweigniederlassung Chur"]
    }
  ]
}
```

## Session-Management

Nach erfolgreichem Login wird `session.json` im Arbeitsverzeichnis gespeichert und bei folgenden Aufrufen wiederverwendet.

Session zurücksetzen (z.B. nach Passwortänderung):
```bash
rm session.json
```
