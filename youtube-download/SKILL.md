---
name: youtube-download
description: Lädt YouTube-Videos als MP3-Audiodatei herunter. Verwende diesen Skill wenn jemand ein YouTube-Video als Audio haben möchte, MP3 aus YouTube braucht, oder einen YouTube-Link in Musik umwandeln will.
---

# YouTube Download Skill

YouTube-Videos als MP3 herunterladen via `yt-dlp` und `ffmpeg`.

## Voraussetzungen

ffmpeg muss installiert sein (apt install ffmpeg / brew install ffmpeg)

## Verwendung

```bash
scripts/yt2mp3.py <youtube-url> [ausgabe-verzeichnis]
```

## Beispiele

```bash
# In aktuelles Verzeichnis herunterladen
scripts/yt2mp3.py "https://www.youtube.com/watch?v=..."

# In bestimmtes Verzeichnis
scripts/yt2mp3.py "https://www.youtube.com/watch?v=..." ~/Music
```

Das Script lädt die beste verfügbare Audioqualität herunter und konvertiert sie zu MP3 (192 kbps). Der Dateiname entspricht dem Video-Titel: `<video-titel>.mp3`

## Upload auf Google Drive

Nach dem Download können MP3s mit `scripts/upload.sh` auf Google Drive hochgeladen werden:

```bash
scripts/upload.sh
```

Dies lädt alle `*.mp3` im aktuellen Verzeichnis auf einen konfigurierten Google Drive Ordner hoch, kopiert sie nach `~/Music` und löscht die lokalen Dateien.
