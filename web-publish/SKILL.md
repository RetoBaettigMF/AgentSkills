---
name: web-publish
description: "Publiziert Dateien und Verzeichnisse auf baettig.org/morticia. Trigger: publizieren, veröffentlichen, online stellen, auf baettig.org hochladen, publish, webseite erstellen."
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

### In Unterverzeichnis deployen

Das Script `--sync-dir` synchronisiert nur ins Root-Verzeichnis `/var/www/html/morticia/`. Für ein eigenes Unterverzeichnis direkt `rsync` verwenden:

```bash
rsync -avz --delete /tmp/mein-projekt/ baettig@baettig.org:/var/www/html/morticia/mein-projekt/
```

URL: `https://baettig.org/morticia/mein-projekt/`

### Verzeichnis löschen

`--delete` löscht nur einzelne Dateien, keine Verzeichnisse (fehlschlag: "Is a directory"). Workaround: erst alle Dateien einzeln löschen, dann das leere Verzeichnis mit `rmdir`:

```bash
# Alle Dateien im Unterverzeichnis löschen
for f in $(ssh baettig@baettig.org "ls /var/www/html/morticia/mein-projekt/"); do
  scripts/morticia-publish --delete "mein-projekt/$f"
done
# Leeres Verzeichnis entfernen
ssh baettig@baettig.org "rmdir /var/www/html/morticia/mein-projekt"
```

### KI-lesbare Assets mitpublizieren

Für Brand-Seiten, Styleguides und andere wiederverwendbare Daten: immer eine `brand.json` (strukturiert) und `brand.txt` (plain text) mit ins Verzeichnis legen. So können KI-Tools die Daten direkt per URL konsumieren (z.B. in Prompts: "Verwende die Brand Guidelines von https://baettig.org/morticia/cudos-design/brand.json"). Siehe `references/ai-readable-publishing.md`.

## Typischer Workflow

1. HTML-Bericht oder Webseite lokal erstellen
2. Mit `scripts/morticia-publish` hochladen (Root) oder `rsync` direkt für Unterverzeichnisse
3. URL an Empfänger weitergeben: `https://baettig.org/morticia/<dateiname>`