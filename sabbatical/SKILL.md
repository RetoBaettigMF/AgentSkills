---
name: sabbatical
description: Search, query, and add information to a personal markdown knowledge base about the user's sabbatical in China. Uses an LLM-generated index plus vector-based RAG over markdown files (contacts, planning, meetings, research, accommodation, etc.). Use when answering questions about the China sabbatical or when storing new information related to it.
---

# Sabbatical Skill

Manages the user's China sabbatical knowledge base, stored as Markdown files in Google Drive.

## Data location

All markdowns live in: `/Users/morticiamac/Google Drive/Meine Ablage/Markdowns`

Two artifacts are maintained alongside the source files:

- `<MARKDOWNS_PATH>/index.md` — human-readable index, rebuilt from `summary_cache.json` on every run
- `summary_cache.json` (next to `scripts/`) — per-file summary cache `{path: {mtime, summary}}`. `update-index` only re-summarizes new/changed files
- `vector_db.json` (next to `scripts/`) — JSON vector DB `{path: {mtime, vector}}`. The file content is NOT stored; only its embedding.

## Scripts

### `scripts/update-index`

Incrementally maintains `summary_cache.json`:
- New file → summarize and add
- Existing file with changed `mtime` → re-summarize
- Existing file with same `mtime` → skip
- File no longer on disk → remove entry
- Previously failed file (no summary) → retry

After updating the cache it rebuilds `index.md` inside the Markdowns folder. Safe to call from a cron job.

```
scripts/update-index
```

### `scripts/update-rag`

Updates `vector_db.json` incrementally:
- New file → embed and add
- Existing file with changed `mtime` → re-embed
- Existing file with same `mtime` → skip
- File no longer on disk → remove entry

Whole-file embeddings (no chunking). Safe to call from a cron job.

```
scripts/update-rag
```

### `scripts/search`

Search the knowledge base. Returns each matching file's full content together with its absolute path (sources). Combines vector similarity from `vector_db.json` with an LLM lookup against `index.md`.

```
scripts/search "When do I fly to Shanghai?"
scripts/search "contacts at Swissnex" --top-k 3
scripts/search "Tsinghua meeting notes" --json
```

`--json` emits a JSON array of `{path, rel_path, score, content}` — preferred when an agent is calling the script.

### `scripts/add-info`

Propose how to store a new piece of information. The script:

1. Calls the search function for similar existing files.
2. If the top match scores above the similarity threshold, asks the LLM to merge the new info into that file and returns a unified diff (`type: "modify"`).
3. Otherwise asks the LLM to propose a new file (filename + content) and returns a creation diff (`type: "create"`).

The script ONLY proposes diffs; the calling agent decides whether to apply them. Output is JSON: `{type, path, rel_path, diff, new_content}`.

```
scripts/add-info "Met Dr. Wang at Tsinghua on 2026-05-12, email wang@tsinghua.edu.cn, works on AI safety"
echo "long content..." | scripts/add-info -
```

## Configuration

Copy `scripts/.env.example` to `scripts/.env` and fill in:

- `OPENROUTER_API_KEY` — for LLM calls (summaries, index lookup, diff generation)
- `OPENROUTER_MODEL` — e.g. `deepseek/deepseek-v4-flash`
- `EMBEDDING_API_KEY` — for embeddings (OpenAI key by default; OpenRouter does not currently expose an embeddings endpoint)
- `EMBEDDING_MODEL` — e.g. `text-embedding-3-small`
- `EMBEDDING_BASE_URL` — defaults to `https://api.openai.com/v1`
- `MARKDOWNS_PATH` — override the default location if needed

## Cron setup (Hermes cronjob system)

The Hermes `cronjob` tool requires scripts under `~/.hermes/scripts/`. Copy the two wrapper scripts from this skill's `scripts/` directory:

```bash
cp scripts/cron-update-rag.sh ~/.hermes/scripts/sabbatical-update-rag.sh
cp scripts/cron-update-index.sh ~/.hermes/scripts/sabbatical-update-index.sh
chmod +x ~/.hermes/scripts/sabbatical-update-rag.sh ~/.hermes/scripts/sabbatical-update-index.sh
```

Then create the cron jobs via `cronjob(action='create', ...)`:
- **Sabbatical RAG Update**: `schedule='0 6 * * *'`, `script='sabbatical-update-rag.sh'`, `no_agent=true`
- **Sabbatical Index Update**: `schedule='5 6 * * *'`, `script='sabbatical-update-index.sh'`, `no_agent=true`

Use `deliver='local'` to avoid spamming the user. Note: `no_agent` script jobs may show `last_status: null` after running — this is a cosmetic tracking quirk; verify by running the wrapper scripts directly instead.

## Insights directory

`Insights/` contains cross-cutting insight documents synthesized from all meeting protocols and research notes. Each insight file has: title, short description, and verbatim quotes with clickable references to source documents. 13 insight themes (Innovationstempo, Fehlerkultur, Guanxi, SuperApps, etc.). When asked to analyze the knowledge base thematically, read these first before re-synthesizing from scratch. See `references/insights-overview.md` for the full list.

To create new insights from the full corpus: (1) run `update-index` to ensure fresh index, (2) read all relevant source files via `read_file` (NOT `search --json` — too large), (3) identify recurring themes across documents, (4) create one `.md` per theme under `Insights/` with title, Kurzbeschreibung, and Zitate mit Referenzen, (5) run `update-index` afterward to index the new files.

## Usage pitfalls

- **Re-index after manual file creation**: `scripts/add-info` auto-triggers a re-index, but when you create or write files directly (e.g. into `Insights/`), you must run `scripts/update-index` afterward so the index and RAG pick them up.

- **Search truncation**: `search --json` returns full file content per hit. With 10+ rich markdown files this routinely exceeds 50K chars and gets truncated. Pattern: use `--top-k N` (e.g. 5) for a scan, then `read_file` the specific files you need for complete content. Do not rely on search alone for comprehensive analysis.
- **Memory budget**: Sabbatical session analysis can be token-heavy. When the agent's memory is near-full, compress or consolidate entries before adding sabbatical pointers.

## Requirements

- `uv` — dependencies are managed automatically via inline script metadata
- OpenRouter account for chat models
- OpenAI-compatible embeddings endpoint (default: OpenAI)
