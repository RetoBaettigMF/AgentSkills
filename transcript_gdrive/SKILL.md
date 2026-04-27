# transcript-gdrive

Monitors a Google Drive folder for new audio files and transcribes them automatically using Whisper. Moves processed files through an inbox → progress → done workflow entirely within Google Drive.

## How it works

```
gog drive ls --parent <inbox>
        ↓ (audio file found, mimeType starts with "audio/")
gog drive move → progress/
        ↓
download to local temp dir
        ↓
whisper transcribe → <basename>.txt
        ↓
gog drive upload .txt → done/
gog drive move audio  → done/
```

The service runs as a systemd user service, starts automatically at boot, and writes logs to the systemd journal.

## Prerequisites

- [`gog`](https://github.com/reto-bättig/gogcli) CLI with Google Drive access
- `jq` for JSON parsing (`sudo apt install jq`)
- Whisper skill at `../whisper/scripts/transcribe` (sibling directory)

## Google Drive Folder IDs

| Folder     | ID                                    |
|------------|---------------------------------------|
| Inbox      | `1dTribE31RQ7bCvQ4_r3eZ9Y2O5rXsyUJ`  |
| progress/  | `10PoANPn2XmjbJSOQrS63COWzzixXS1eL`  |
| done/      | `1ky0E9E8Cn242tFOOX5atOOzVh2528p5e`  |

## Usage

### One-shot (process all current files and exit)

```bash
./scripts/transcribe_once
```

### Continuous loop (manual, checks every 60s)

```bash
./scripts/transcribe_loop
```

### As a systemd service (recommended)

```bash
chmod +x install uninstall scripts/transcribe_once scripts/transcribe_loop
./install
```

## Uninstall

```bash
./uninstall
```

## Service management

```bash
# Status and recent logs
./install --status

# Live log stream
journalctl --user -u transcript-gdrive -f

# Restart / stop / start
systemctl --user restart transcript-gdrive
systemctl --user stop    transcript-gdrive
systemctl --user start   transcript-gdrive
```

## Files

| File                        | Description                                      |
|-----------------------------|--------------------------------------------------|
| `scripts/transcribe_once`   | Check inbox once, process all found audio files  |
| `scripts/transcribe_loop`   | Run `transcribe_once` in a loop every 60 seconds |
| `install`                   | Install as systemd user service                  |
| `uninstall`                 | Remove systemd user service                      |
