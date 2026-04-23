---
name: rechnungskontrolle
description: Vollständige Rechnungskontrolle und -abstimmung durch Abgleich von Bexio-Rechnungen mit RolX-Stunden. Use when user asks to verify an invoice, check invoice hours, "Rechnung prüfen", "Rechnung kontrollieren", "Rechnung gegen Stunden abgleichen", "Rechnungsabstimmung", or invoice reconciliation. Combines bexio and rolx skills.
---

# Rechnungskontrolle Skill

Durchführung einer vollständigen Rechnungskontrolle durch Abgleich von Bexio-Rechnungen mit den erfassten Arbeitsstunden aus RolX.

Verwende für die Kontrolle die bestehenden Skills "rolx" und "bexio"
Informiere den User, falls ess die Skills nicht gibt.

### Schritt 1: Rechnung aus Bexio laden

Hole die Rechnung anhand der Rechnungsnummer.
Rechnungsnummern haben das folgende Format:
`#0158.003.01.01`

**Aus der Rechnung extrahieren:**
- Auftragsnummer (z.B. `#0158.003`) — ist identisch mit der Projektnummer in RolX
- Rechnungszeitraum (Monat/Jahr)
- Stunden pro Aufgabe/Mitarbeiter/Phase etc. 

### Schritt 2: Stunden aus RolX abfragen

Abfrage der erfassten Stunden für denselben Zeitraum mit der Auftragsnummer.
Frage auch gleich pro Aufgabe, pro Mitarbeiter und gib zusätzlich für jede Aufgabe auch die Verrechnungsart an.
Beispiel: "Gib mir die Summe der Stunden vom Auftrag `#0158.003` pro Aufgabe und pro Mitarbeiter im Juni 2026 inklusive der Verrechnungsart"


### Schritt 3: Details pro Aufgabe prüfen (bei Abweichungen)

Falls Unterschiede zwischen Rechnung und RolX-Stunden bestehen, mehr details von RolX abfragen (aufgaben, mitarbeiter und verrechnungsart)

## Was wird geprüft

- Stimmen die auf der Rechnung ausgewiesenen Stunden mit den in RolX erfassten überein?
- Sind alle erfassten Stunden auch berechnet worden?
- Gibt es Stunden auf der Rechnung, die nicht in RolX erfasst sind?
- Sind die Stundensätze korrekt angewendet?

## Unterstützende Skills

Dieser Skill nutzt intern die Fähigkeiten der folgenden Skills:
- **bexio** — für den Zugriff auf Kundenrechnungen
- **rolx** — für den Zugriff auf die Zeiterfassung
