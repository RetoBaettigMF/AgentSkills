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

Weitere Informationen zum AgentSkills-Standard findest du unter: https://agentskills.io/
