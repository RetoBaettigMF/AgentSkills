# AgentSkills

Dieses Repository enthält verschiedene **Agent Skills**, entwickelt nach dem Muster von [AgentSkills.io](https://agentskills.io/).

## Was sind Agent Skills?

Agent Skills sind modulare, selbstständige Pakete, die die Fähigkeiten von AI-Agents erweitern. Sie bieten:

- **Spezialisierte Workflows** – Mehrschritt-Verfahren für spezifische Domänen
- **Tool-Integrationen** – Anleitungen für den Umgang mit spezifischen Dateiformaten oder APIs
- **Domänen-Expertise** – Unternehmensspezifisches Wissen, Schemas, Geschäftslogik
- **Gebündelte Ressourcen** – Skripte, Referenzen und Assets für komplexe Aufgaben

## Struktur der Skills

Jeder Skill folgt einer standardisierten Struktur:

```
skill-name/
├── SKILL.md              # Hauptdokumentation (YAML-Frontmatter + Markdown)
├── scripts/              # Ausführbare Skripte (Python/Bash/etc.)
├── references/           # Dokumentation für Context-Loading
└── assets/               # Dateien für Output (Templates, Icons, etc.)
```

## Enthaltene Skills

### [answer-emails](answer-emails/)

Beantwortet ungelesene Emails automatisch. Klassifiziert Emails (Weiterleitungen von Reto, Aufträge an den Bot, alle anderen) und antwortet entsprechend — inklusive Archivierung und Label-Verwaltung via gogcli.

**Trigger:** „beantworte Emails", „check Emails", „AnswerEmails", „ungelesene Emails bearbeiten"

---

### [bexio](bexio/)

Abfrage von Kundenrechnungen und Finanzdaten über die Bexio-Integration des CudosControlling Tools. Ermöglicht den Zugriff auf Rechnungen im Format `#XXXX.YYY.ZZ.VV`.

**Trigger:** „Rechnung", „Zeige Rechnung", „Bexio", „bills"

---

### [crm](crm/)

Abfrage von Kontakten, Firmen, Verkaufschancen und Kommentaren aus berliCRM via REST API. Unterstützt Suche, Detailabfragen und direkte SQL-ähnliche Queries.

**Trigger:** CRM-Daten, Kundenkontakte, Accounts, Potentials, Kommentare, direkte CRM-Abfragen

---

### [cudos-trail-profile](cudos-trail-profile/)

Erstellt und versendet personalisierte Emails mit passenden CudosTrail-Kandidatenprofilen (PDFs) an Kunden. Liest Anweisungen aus eingehenden Emails, wählt Profile aus Google Drive aus und sendet die fertige Email zurück an Reto zum Weiterleiten.

**Trigger:** „CudosTrail Profile senden", „Juniors anbieten", „Profile für Kunden", „CT Profile"

---

### [daily-sales-input](daily-sales-input/)

Erstellt täglich 1–2 konkrete Firmenkontakte für Kalt- oder Warmakquisition (Cudos AG). Recherchiert via CRM, Moneyhouse und News, filtert nach Potential und Distanz, und versendet den strukturierten Sales-Input per Email.

**Trigger:** „Daily Sales Input", „täglicher Sales Input", „Sales Input erstellen"

---

### [gogcli](gogcli/)

CLI für Gmail, Calendar, Drive, Sheets, Docs, Contacts, Tasks, Chat und weitere Google Workspace-Dienste. Basis-Skill für alle Google-Integrationen mit JSON-Output-Unterstützung und Multi-Account-Handling.

**Trigger:** Jede Interaktion mit Google Workspace (Email senden, Kalender abfragen, Drive verwalten, Sheets lesen/schreiben etc.)

---

### [moneyhouse](moneyhouse/)

Automatisiertes Auslesen von Firmeninformationen von moneyhouse.ch via Browser-Automatisierung und LLM-basierter Datenextraktion. Liefert strukturierte JSON-Daten zu Schweizer Unternehmen.

**Trigger:** Firmendetails, Handelsregisterinformationen, Mitarbeiterzahlen, Zeichnungsberechtigte, Rechtsformen

---

### [rechnungskontrolle](rechnungskontrolle/)

Vollständige Rechnungskontrolle durch Abgleich von Bexio-Rechnungen mit den in RolX erfassten Arbeitsstunden. Kombiniert die Skills `bexio` und `rolx`.

**Trigger:** „Rechnung prüfen", „Rechnung kontrollieren", „Rechnung gegen Stunden abgleichen", „Rechnungsabstimmung", invoice reconciliation

---

### [rolx](rolx/)

Zeiterfassung und Projektstunden aller Cudos-Mitarbeitenden via RolX-Integration. Unterstützt Abfragen nach Mitarbeiter, Projekt oder Zeitraum.

**Trigger:** Fragen über Projektstunden, Zeiterfassungsdaten, Arbeitsstunden oder „RolX"

---

### [sales-outreach](sales-outreach/)

Erstellt personalisierte Kaltakquise-Emails für Cudos AG nach bewährter Vorlage: persönliche Einleitung, KI-Value-Proposition und konkreter CTA mit Calendly-Link.

**Trigger:** „Sales Outreach Email schreiben", „Kaltakquise Email", „Outreach Template", „Email an potenzielle Kunden"

---

### [termin-vorbereitung](termin-vorbereitung/)

Erstellt ein tägliches Briefing für Kundentermine: Kalenderabfrage, CRM-Recherche (Kommentare + Potentiale) und Zusammenfassung mit Empfehlungen per Email.

**Trigger:** „Terminvorbereitung", „Briefing für morgen", „Meeting vorbereiten", „was habe ich morgen für Termine"

---

### [update-sales-pipeline](update-sales-pipeline/)

Führt den Sales-Report aus und aktualisiert das Google Sheet mit der Sales-Pipeline. Informiert das Team per Email mit Link und Zusammenfassung der Resultate.

**Trigger:** „Sales Pipeline updaten", „Sales Report ausführen", „Pipeline aktualisieren", „Update Sales Pipeline"

---

### [web-publish](web-publish/)

Publiziert Dateien und Verzeichnisse auf `https://baettig.org/morticia/` via SSH/SCP/rsync. Unterstützt Einzeldateien, Verzeichnis-Sync und automatische Index-Erstellung.

**Trigger:** „publizieren", „veröffentlichen", „online stellen", „auf baettig.org hochladen", „publish"

---

### [weekly-report](weekly-report/)

Erstellt den wöchentlichen Bericht für Reto Bättig: RolX-Stunden der letzten Woche zusammenfassen, Kalendertermine der nächsten Woche auflisten, Bericht formatieren und per Email + WhatsApp senden.

**Trigger:** „Wochenreport", „Weekly Report", „Wochenbericht erstellen"

---

### [whisper](whisper/)

Transkribiert Audiodateien (MP3, WAV, M4A, FLAC etc.) via OpenAI Whisper API. Unterstützt Deutsch, Englisch und weitere Sprachen.

**Trigger:** Audiodatei transkribieren, Sprachaufnahme in Text umwandeln, „whisper"

---

### [youtube-download](youtube-download/)

Lädt YouTube-Videos als MP3-Audiodateien herunter (192 kbps) via `yt-dlp` und `ffmpeg`. Optional mit Upload auf Google Drive.

**Trigger:** YouTube-Video als Audio, MP3 aus YouTube, YouTube-Link in Musik umwandeln

---

Weitere Informationen zum AgentSkills-Standard findest du unter: https://agentskills.io/
