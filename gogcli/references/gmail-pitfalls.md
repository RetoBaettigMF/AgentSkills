# Gmail Send Pitfalls & Workarounds

## Long body with special characters

`gog gmail send --body "..."` fails when the body contains shell-special characters
(`&`, `'`, `"`) or is very long (>4KB). The shell interprets `&` as backgrounding.

### Workaround A: Pipe from file
```bash
gog gmail send --to <recipient> --subject "<subject>" --body "$(cat /tmp/body.txt | head -c 3500)"
```

### Workaround B: Python subprocess (recommended for long/complex bodies)
```python
import subprocess
with open('/tmp/body.txt', 'r') as f:
    body = f.read()
result = subprocess.run(
    ['gog', 'gmail', 'send', '--to', 'reto.baettig@cudos.ch',
     '--subject', subject, '--body', body],
    capture_output=True, text=True, timeout=30
)
```
This avoids all shell escaping issues since arguments are passed as a list.

Note: gog may time out with very long bodies. Keep under ~3500 chars.

## Drive Flags (easy to get wrong)

| Operation | Flag | Example |
|---|---|---|
| List folder contents | `--parent <folderId>` | `gog drive ls --parent 1fZwa... --json` |
| Download file | `--out <path>` | `gog drive download <fileId> --out ~/local.md` |
| Search | `--query <Drive query>` | `gog drive ls --query "name contains 'Memory'"` |
