"""Shared helpers for the sabbatical skill.

Loaded by all CLI scripts via ``sys.path`` injection. Each calling script must
list ``openai`` and ``python-dotenv`` in its inline uv script dependencies.
"""

import difflib
import json
import math
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DB_PATH = SKILL_DIR / "vector_db.json"
SUMMARY_CACHE_PATH = SKILL_DIR / "summary_cache.json"
DEFAULT_MARKDOWNS = "/Users/morticiamac/Google Drive/Meine Ablage/Markdowns"
SIMILARITY_THRESHOLD = 0.55
SUMMARY_MAX_CHARS = 8000
EMBED_MAX_CHARS = 30000


def load_env():
    load_dotenv(SCRIPT_DIR / ".env")


def _require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} is not set. Check {SCRIPT_DIR / '.env'}.")
    return value


def get_chat_client() -> OpenAI:
    return OpenAI(
        base_url=os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        api_key=_require("OPENROUTER_API_KEY"),
    )


def get_chat_model() -> str:
    return os.environ.get("OPENROUTER_MODEL", "deepseek/deepseek-v4-flash")


def get_embedding_client() -> OpenAI:
    return OpenAI(
        base_url=os.environ.get("EMBEDDING_BASE_URL", "https://api.openai.com/v1"),
        api_key=_require("EMBEDDING_API_KEY"),
    )


def get_embedding_model() -> str:
    return os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")


def get_markdowns_path() -> Path:
    p = Path(os.environ.get("MARKDOWNS_PATH", DEFAULT_MARKDOWNS))
    if not p.exists():
        raise FileNotFoundError(f"Markdowns folder not found: {p}")
    return p


def iter_markdown_files(root: Path):
    """Yield every .md file under root, except index.md at the top level."""
    for path in sorted(root.rglob("*.md")):
        if path.name == "index.md" and path.parent == root:
            continue
        yield path


def cosine(a, b) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0


def embed_text(text: str) -> list[float]:
    client = get_embedding_client()
    resp = client.embeddings.create(model=get_embedding_model(), input=text[:EMBED_MAX_CHARS])
    return resp.data[0].embedding


def load_db() -> dict:
    if DB_PATH.exists():
        return json.loads(DB_PATH.read_text(encoding="utf-8"))
    return {}


def save_db(db: dict) -> None:
    DB_PATH.write_text(json.dumps(db), encoding="utf-8")


def load_summary_cache() -> dict:
    if SUMMARY_CACHE_PATH.exists():
        return json.loads(SUMMARY_CACHE_PATH.read_text(encoding="utf-8"))
    return {}


def save_summary_cache(cache: dict) -> None:
    SUMMARY_CACHE_PATH.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _strip_code_fence(text: str) -> str:
    text = text.strip()
    m = re.match(r"^```(?:[a-zA-Z0-9_+-]*)\n(.*)\n```$", text, re.DOTALL)
    if m:
        return m.group(1)
    return text


def _llm_chat(prompt: str, max_tokens: int = 1024) -> str:
    client = get_chat_client()
    resp = client.chat.completions.create(
        model=get_chat_model(),
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
    )
    content = resp.choices[0].message.content
    if not content:
        raise RuntimeError(f"chat model returned empty content (finish_reason={resp.choices[0].finish_reason!r})")
    return content.strip()


def summarize_file(rel_path: str, content: str) -> str:
    if not content.strip():
        return "(empty file)"
    prompt = (
        "Summarize what kind of information can be found in this markdown file "
        "in 1-2 concise sentences. Focus on topics and content, not formatting.\n\n"
        f"File: {rel_path}\n\nContent:\n{content[:SUMMARY_MAX_CHARS]}"
    )
    return _llm_chat(prompt, max_tokens=200)


def query_index_for_files(query: str, root: Path) -> list[str]:
    """Ask the LLM which files from index.md look relevant."""
    index_path = root / "index.md"
    if not index_path.exists():
        return []
    index_content = index_path.read_text(encoding="utf-8", errors="replace")
    prompt = (
        "You are given an index of markdown files and a user query. "
        "Return ONLY a JSON array of up to 3 relative file paths from the index "
        "that are most likely to contain relevant information. "
        "If none look relevant, return [].\n\n"
        f"INDEX:\n{index_content}\n\nQUERY: {query}\n"
    )
    try:
        text = _strip_code_fence(_llm_chat(prompt, max_tokens=300))
        result = json.loads(text)
        if isinstance(result, list):
            return [str(x) for x in result]
    except Exception as e:
        print(f"Warning: index lookup failed: {e}", file=sys.stderr)
    return []


def search(query: str, top_k: int = 5) -> list[dict]:
    """Return matching files with full content + absolute paths."""
    root = get_markdowns_path()
    db = load_db()
    scored: list[tuple[float, str]] = []
    if db:
        qvec = embed_text(query)
        for key, entry in db.items():
            scored.append((cosine(qvec, entry["vector"]), key))
        scored.sort(reverse=True)

    index_suggested = query_index_for_files(query, root)

    seen: dict[str, float] = {}
    for score, key in scored[:top_k]:
        seen[key] = score
    for key in index_suggested:
        seen.setdefault(key, 0.0)

    results: list[dict] = []
    for key, score in sorted(seen.items(), key=lambda kv: -kv[1]):
        f = root / key
        if not f.exists():
            continue
        results.append({
            "path": str(f),
            "rel_path": key,
            "score": score,
            "content": f.read_text(encoding="utf-8", errors="replace"),
        })
    return results


def _unified_diff(old: str, new: str, fromfile: str, tofile: str) -> str:
    return "\n".join(difflib.unified_diff(
        old.splitlines(),
        new.splitlines(),
        fromfile=fromfile,
        tofile=tofile,
        lineterm="",
    ))


def propose_diff(new_info: str) -> dict:
    """Find similar file or propose new file; return a diff proposal."""
    root = get_markdowns_path()
    results = search(new_info, top_k=3)

    top = results[0] if results else None
    if top and top["score"] >= SIMILARITY_THRESHOLD:
        prompt = (
            "You are updating a markdown knowledge base. Integrate the new "
            "information into the existing file below. Output ONLY the full "
            "updated file content, no explanations and no code fences. "
            "If the file is genuinely not a good fit for the new information, "
            "output exactly the single token NO_MATCH.\n\n"
            f"NEW INFORMATION:\n{new_info}\n\n"
            f"EXISTING FILE ({top['rel_path']}):\n{top['content']}\n"
        )
        new_content = _strip_code_fence(_llm_chat(prompt, max_tokens=4000))
        if new_content.strip() == "NO_MATCH":
            return _propose_new_file(new_info, results, root)
        return {
            "type": "modify",
            "path": top["path"],
            "rel_path": top["rel_path"],
            "diff": _unified_diff(top["content"], new_content, top["rel_path"], top["rel_path"]),
            "new_content": new_content,
        }

    return _propose_new_file(new_info, results, root)


def _propose_new_file(new_info: str, existing_results: list[dict], root: Path) -> dict:
    existing_titles = "\n".join(f"- {r['rel_path']}" for r in existing_results) or "(none)"
    prompt = (
        "You are creating a new markdown file in a knowledge base. "
        "Return ONLY a JSON object (no code fences) with keys 'filename' and 'content'. "
        "'filename' must be a single filename (e.g. 'Topic.md') matching the style "
        "of the existing files. 'content' is the full markdown body.\n\n"
        f"INFORMATION TO STORE:\n{new_info}\n\n"
        f"EXISTING FILE NAMES (style reference):\n{existing_titles}\n"
    )
    raw = _strip_code_fence(_llm_chat(prompt, max_tokens=4000))
    proposal = json.loads(raw)
    filename = proposal["filename"]
    content = proposal["content"]
    new_path = root / filename
    return {
        "type": "create",
        "path": str(new_path),
        "rel_path": filename,
        "diff": _unified_diff("", content, "/dev/null", filename),
        "new_content": content,
    }
