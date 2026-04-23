---
name: web-publish
description: Publiziert Dateien und Verzeichnisse auf baettig.org/morticia. Verwende diesen Skill um Webseiten, HTML-Dateien, Berichte oder andere Dateien öffentlich zugänglich zu machen. Trigger: "publizieren", "veröffentlichen", "online stellen", "auf baettig.org hochladen", "publish", "webseite erstellen".
---

# Morticia Skill

Dateien und Verzeichnisse auf `https://baettig.org/morticia/` publizieren via SSH/SCP/rsync.

## Voraussetzungen

SSH-Zugriff auf `baettig@baettig.org` muss eingerichtet sein (SSH-Key).

## Verwendung

```bash
scripts/morticia-publish <datei(en)>
scripts/morticia-publish --list
scripts/morticia-publish --sync-dir <verzeichnis>
scripts/morticia-publish --delete <dateiname>
scripts/morticia-publish --index ["Titel"]
```

## Befehle

### Dateien publizieren
```bash
scripts/morticia-publish bericht.html
scripts/morticia-publish index.html style.css app.js
```
Nach dem Upload verfügbar unter: `https://baettig.org/morticia/<dateiname>`

### Publizierte Dateien auflisten
```bash
scripts/morticia-publish --list
```

### Ganzes Verzeichnis synchronisieren
```bash
scripts/morticia-publish --sync-dir ./meine-webseite/
```
Alle Dateien werden mit `rsync --delete` synchronisiert. Basis-URL: `https://baettig.org/morticia/`

### Datei löschen
```bash
scripts/morticia-publish --delete alte-datei.html
```

### Index-Seite erstellen
```bash
scripts/morticia-publish --index
scripts/morticia-publish --index "Meine Berichte"
```
Erstellt eine `index.html` mit Links zu allen publizierten Dateien.

## Typischer Workflow

1. HTML-Bericht oder Webseite lokal erstellen
2. Mit `scripts/morticia-publish` hochladen
3. URL an Empfänger weitergeben: `https://baettig.org/morticia/<dateiname>`
