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

## Pitfalls

### 403 Forbidden nach rsync-Upload

Nach `rsync` in ein neues/aktualisiertes Unterverzeichnis kann die URL `403 Forbidden` liefern. Zwei mögliche Ursachen — in dieser Reihenfolge prüfen:

**1. Datei-Permissions (häufigster Fall):** rsync erstellt Dateien oft mit `600` (`-rw-------`) statt `644` (`-rw-r--r--`). Apache (www-data) kann sie dann nicht lesen.
```bash
# Prüfen:
ssh baettig@baettig.org "ls -la /var/www/html/morticia/mein-projekt/"
# Fixen:
ssh baettig@baettig.org "chmod 644 /var/www/html/morticia/mein-projekt/*"
```
Vorher/Nachher mit lokalem curl verifizieren:
```bash
ssh baettig@baettig.org "curl -sI http://localhost/morticia/mein-projekt/ | head -5"
```

**2. Cloudflare-Proxy-Cache:** Wenn lokal bereits 200 kommt, aber extern noch 403, kurz warten (5–10s) und erneut testen. Löst sich von selbst.

## Templates

- `templates/audio-player.html` — Self-contained HTML audio player page with track listing, play/pause, configurable skip buttons (±2s/±5s/±10s), progress bar, volume control, auto-advance, and keyboard shortcuts. Dark theme, mobile-responsive. Designed for hosting alongside MP3 files in the same directory. Includes the mute-before-seek pattern to avoid audible glitches.
- `references/audio-player-multi-tab.md` — How to extend the single-set template to support multiple tabbed track collections (e.g. textbook + workbook) sharing one player bar.

## Typischer Workflow

1. HTML-Bericht oder Webseite lokal erstellen
2. Mit `scripts/morticia-publish` hochladen (Root) oder `rsync` direkt für Unterverzeichnisse
3. Bei 403: Siehe [Pitfalls → 403 Forbidden](#403-forbidden-nach-rsync-upload) — zuerst Permissions prüfen, dann Cloudflare-Cache
4. URL an Empfänger weitergeben: `https://baettig.org/morticia/<dateiname>`