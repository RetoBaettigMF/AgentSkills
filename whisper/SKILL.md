---
name: whisper
description: Transcribe audio files (MP3, WAV/PCM) using OpenAI Whisper API. Use when you need to convert speech to text from audio recordings, voice messages, or any audio file. Supports German, English, and other languages.
---

# Whisper Skill

Transcribe audio files using OpenAI's Whisper speech-to-text API.

## Supported Formats

- MP3
- WAV/PCM
- M4A, FLAC, OGG, WEBM, MP4, MPEG

## Usage

```bash
scripts/transcribe <audio_file> [options]
```

Options:
- `--language` - Language code (e.g., `de`, `en`)
- `--api-key` - OpenAI API key (or set `OPENAI_API_KEY` env var)
- `--model` - Model to use (default: `whisper-1`)

## Examples

```bash
# Basic transcription
scripts/transcribe recording.mp3

# German language
scripts/transcribe voice.wav --language de

# With explicit API key
scripts/transcribe audio.mp3 --api-key sk-xxx
```

## Requirements

- `uv` — dependencies are managed automatically via inline script metadata
- `OPENAI_API_KEY` environment variable or `--api-key` argument
