---
name: termin-vorbereitung
description: Erstelle ein tägliches Briefing für Kundentermine von Reto Bättig: Kalenderabfrage, CRM-Recherche (Kommentare + Potentiale), Zusammenfassung mit Empfehlungen, Email-Versand. Verwende diesen Skill für "Terminvorbereitung", "Briefing für morgen", "Meeting vorbereiten", "was habe ich morgen für Termine".
---

# Terminvorbereitung

Erstellt ein tägliches Briefing für Kundentermine.

## Vorgehen

1. **Kalender abfragen** — Termine von reto.baettig@cudos.ch für den angegebenen Tag (falls nichts spezifiziert: morgigen Tag):
   ```bash
   gog calendar events reto.baettig@cudos.ch --tomorrow
   ```

2. **Filtern** — Ignoriere alle Meetings, die ausschliesslich mit Personen von cudos.ch stattfinden

3. **Für jedes externe Meeting:**
   - Suche die Person im CRM und ermittle ihre Firma 
   - Hole eine Zusammenfassung aller Kommentare zur Firma aus den letzten 2 Jahren
   - Hole eine Zusammenfassung aller offenen Potentiale der Firma

4. **Briefing erstellen** — Fasse alles zu einem Briefing mit Empfehlungen für die Ziele des Meetings zusammen

5. **Versenden** — Sammle alle Briefings und sende sie per Email an reto.baettig@cudos.ch
