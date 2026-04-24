---
name: weekly-report
description: Erstelle den wöchentlichen Bericht für Reto Bättig: RolX-Stunden der letzten Woche zusammenfassen, Kalendertermine der nächsten Woche auflisten, Bericht formatieren und per Email + WhatsApp senden. Verwende diesen Skill für "Wochenreport", "Weekly Report", "Wochenbericht erstellen".
---

# Wochenreport erstellen

Erstellt den Wochenreport in 4 Schritten.

## Definitionen
- **Letzte Woche**: Gehe zum letzten Montag zurück → +7 Tage = Ende der letzten Woche
- **Nächste Woche**: Die 7 Tage von Montag bis Sonntag, die auf die letzte Woche folgen

---

## Schritt 1: Ereignisse der letzten Woche (RolX)

Hole alle Einträge von Reto Bättig aus RolX mit Kommentar. Fasse sie in folgenden Kategorien zusammen:

- Kundenkontakt
- Sales, Offerten, Telefonieren etc. (inhouse)
- Projekte
- Strategie/Marketing/Geschäftsleitung etc.
- Marketing/Strategie/Auswertungen etc.
- Mitarbeiter
- Diverses
- IT
- Top-Erfolge dieser Woche *(nur explizit als solche markierte Einträge)*
- Strategie-Wirkung dieser Woche *(nur explizit als solche markierte Einträge)*

**Formatierungsregeln:**
- Ausgabe als Markdown ohne Titel-Überschrift
- Mehrfache Eintragungen zusammenfassen
- activityNames, Datum und Zeiten weglassen
- Leere Kategorien weglassen
- Alle Kommentare müssen in der Zusammenfassung vorkommen

---

## Schritt 2: Kalendertermine der nächsten Woche

Hole alle Termine aus dem Google Calendar von reto.baettig@cudos.ch für die nächste Woche.

**Formatierung:** Eine Zeile pro Termin, z.B.:
```
- Treffen mit Hans Müller, Firma Zetta
- Telco mit Franz Meier
- Vortrag bei XYZ AG
```

**Regeln:**
- Nur reguläre Termine (keine "Ausser Haus"-Einträge oder Aufgaben)
- Auch wiederkehrende Termine auflisten
- Gleiche Einträge am selben Tag zusammenfassen
- Einträge "Block" oder "Büro" weglassen
- Cudos-interne Weeklys weglassen
- Vollständige Liste ausgeben, keine weiteren Kommentare

---

## Schritt 3: Bericht erstellen und Feedback einholen

Erstelle den Bericht im folgenden Markdown-Format:

```markdown
## Reto
*Letzte Woche*
  - (Infos der letzten Woche)
*Nächste Woche*
  - (Infos der nächsten Woche)
```

Sende den Bericht per Email an reto.baettig@cudos.ch und an den aktiven WhatsApp-Kanal. Frage um Feedback.
Falls Feedback kommt, baue es in den Bericht ein.

---

## Schritt 4 (optional): Bericht ins Meetingprotokoll einfügen

Nur wenn explizit gewünscht: Füge den fertigen Bericht in das Meetingprotokoll ein.
