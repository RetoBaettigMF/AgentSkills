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

### [bexio](bexio/)

Abfrage von Kundenrechnungen und Finanzdaten über die Bexio-Integration des CudosControlling Tools. Ermöglicht den Zugriff auf Rechnungen im Format `#XXXX.YYY.ZZ.VV`.

**Trigger:** „Rechnung", „Zeige Rechnung", „Bexio", „bills"

---

### [rolx](rolx/)

Zeiterfassung und Projektstunden aller Cudos-Mitarbeitenden via RolX-Integration. Unterstützt Abfragen nach Mitarbeiter, Projekt oder Zeitraum.

**Trigger:** Fragen über Projektstunden, Zeiterfassungsdaten, Arbeitsstunden oder „RolX"

---

### [rechnungskontrolle](rechnungskontrolle/)

Vollständige Rechnungskontrolle durch Abgleich von Bexio-Rechnungen mit den in RolX erfassten Arbeitsstunden. Kombiniert die Skills `bexio` und `rolx`.

**Trigger:** „Rechnung prüfen", „Rechnung kontrollieren", „Rechnung gegen Stunden abgleichen", „Rechnungsabstimmung", invoice reconciliation

---

### [crm](crm/)

Abfrage von Kontakten, Firmen, Verkaufschancen und Kommentaren aus berliCRM via REST API. Unterstützt Suche, Detailabfragen und direkte SQL-ähnliche Queries.

**Trigger:** CRM-Daten, Kundenkontakte, Accounts, Potentials, Kommentare, direkte CRM-Abfragen

---

### [moneyhouse](moneyhouse/)

Automatisiertes Auslesen von Firmeninformationen von moneyhouse.ch via Browser-Automatisierung und LLM-basierter Datenextraktion. Liefert strukturierte JSON-Daten zu Schweizer Unternehmen.

**Trigger:** Firmendetails, Handelsregisterinformationen, Mitarbeiterzahlen, Zeichnungsberechtigte, Rechtsformen

---

### [web-publish](web-publish/)

Publiziert Dateien und Verzeichnisse auf `https://baettig.org/morticia/` via SSH/SCP/rsync. Unterstützt Einzeldateien, Verzeichnis-Sync und automatische Index-Erstellung.

**Trigger:** „publizieren", „veröffentlichen", „online stellen", „auf baettig.org hochladen", „publish"

---

### [youtube-download](youtube-download/)

Lädt YouTube-Videos als MP3-Audiodateien herunter (192 kbps) via `yt-dlp` und `ffmpeg`. Optional mit Upload auf Google Drive.

**Trigger:** YouTube-Video als Audio, MP3 aus YouTube, YouTube-Link in Musik umwandeln

---

Weitere Informationen zum AgentSkills-Standard findest du unter: https://agentskills.io/
