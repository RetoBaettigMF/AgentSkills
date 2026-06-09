# gog gmail send — Reply-Patterns

## Reply mit Zitat und CC (Klasse 1)

```bash
# 1. Body in Temp-File schreiben
write_file /tmp/email_reply.txt "<reply body>"

# 2. Senden mit Thread-ID + Quote
gog gmail send \
  --to "<original_sender_email>" \
  --cc "reto.baettig@cudos.ch" \
  --subject "<subject>" \
  --body-file /tmp/email_reply.txt \
  --thread-id <threadId> \
  --quote \
  --account bar.ai.bot@cudos.ch \
  --json
```

## Wichtige Flags

| Flag | Zweck |
|------|-------|
| `--thread-id` | Setzt den Thread fort (besser als `--reply-to-message-id` für Replies) |
| `--quote` | Zitiert die originale Nachricht im Reply |
| `--body-file` | Body aus Datei (vermeidet Shell-Escaping-Probleme) |
| `--cc` | CC-Empfänger (immer reto.baettig@cudos.ch bei Klasse 1) |
| `--reply-to-message-id` | Alternative zu `--thread-id` — setzt In-Reply-To/References Header |

## Entdeckt via

```bash
gog gmail send --help
```
