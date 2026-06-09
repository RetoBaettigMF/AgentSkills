# Telegram Voice Messages

When Reto sends a voice message via Telegram, Hermes receives it as an `.ogg` file
stored in the audio cache.

## File Location

```
~/.hermes/audio_cache/audio_*.ogg
```

Find the most recent file with:

```bash
ls -t ~/.hermes/audio_cache/*.ogg | head -1
```

## Transcription

Use the whisper skill's transcribe script with German language:

```bash
/path/to/whisper/scripts/transcribe <file> --language de
```

## Workflow

1. Voice message arrives via Telegram → Hermes sees STT failure note
2. Find the `.ogg` file in `~/.hermes/audio_cache/`
3. Run whisper transcription
4. Respond to the transcribed content
