---
name: youtube-download
description: Lädt YouTube-Videos als MP3-Audiodatei herunter. Verwende diesen Skill wenn jemand ein YouTube-Video als Audio haben möchte, MP3 aus YouTube braucht, oder einen YouTube-Link in Musik umwandeln will.
---

# YouTube Download Skill

YouTube-Videos als MP3 herunterladen via `yt-dlp` und `ffmpeg`.

## Voraussetzungen

- `ffmpeg` (brew install ffmpeg / apt install ffmpeg)
- `yt-dlp` CLI (brew install yt-dlp / pip install yt-dlp)

> ⚠️ `brew install yt-dlp` installiert NUR den CLI-Befehl, nicht das Python-Modul `yt_dlp`. Das Python-Script `scripts/yt2mp3` funktioniert damit NICHT — immer den CLI-Weg nehmen.

## Verwendung

**Primär: yt-dlp CLI (empfohlen)**

```bash
cd ~/Downloads && yt-dlp -x --audio-format mp3 --audio-quality 192k "<youtube-url>"
```

Kein Python-Modul nötig — der `yt-dlp` CLI-Befehl erledigt alles in einem Schritt.

**Fallback: Python-Script (nur wenn `yt_dlp` als Python-Modul installiert ist)**

```bash
python3 scripts/yt2mp3 "<youtube-url>" ~/Downloads
```

> ⚠️ `scripts/yt2mp3` ist ein Python-Script, das `import yt_dlp` braucht. `brew install yt-dlp` installiert nur den CLI-Befehl, nicht das Python-Modul. Wenn `ModuleNotFoundError: No module named 'yt_dlp'` kommt, nutze den CLI-Weg oben.

## Workflow (vollständig — IMMER beide Schritte)

Schritt 1 und 2 gehören zusammen. Niemals nur Schritt 1 ausführen.

### Schritt 1: Download

```bash
cd ~/Downloads && yt-dlp -x --audio-format mp3 --audio-quality 192k "<youtube-url>"
```

### Schritt 2: Upload + Ablage (PFLICHT)

Nach erfolgreichem Download SOFORT den Upload ausführen. Das Script findet alle `*.mp3` im aktuellen Verzeichnis:

```bash
cd ~/Downloads && bash /Users/morticiamac/Development/AgentSkills/youtube-download/scripts/upload.sh
```

Das Script `upload.sh` macht drei Dinge:
1. Lädt alle `*.mp3` im aktuellen Verzeichnis auf Google Drive hoch
2. Kopiert sie nach `~/Music`
3. Löscht die temporären lokalen Dateien

Nach dem Upload ist die Datei unter `~/Music/<titel>.mp3` und via Google Drive Link verfügbar.
