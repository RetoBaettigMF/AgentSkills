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

## Suggested cron entries

```
0 6 * * * /Users/morticiamac/.hermes/skills/AgentSkills/sabbatical/scripts/update-rag
5 6 * * * /Users/morticiamac/.hermes/skills/AgentSkills/sabbatical/scripts/update-index
```

## Requirements

- `uv` — dependencies are managed automatically via inline script metadata
- OpenRouter account for chat models
- OpenAI-compatible embeddings endpoint (default: OpenAI)
