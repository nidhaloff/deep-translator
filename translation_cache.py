"""Block-level translation cache backed by SQLite.

Stores translated strings keyed by (translator, source, target, model,
text-hash) so re-translating an edited PDF only pays for blocks whose text
actually changed.
"""

import hashlib
import sqlite3
import threading
from pathlib import Path
from typing import Optional


_CACHE_PATH = Path(".cached") / "translations.sqlite3"
_lock = threading.Lock()


def _connect() -> sqlite3.Connection:
    _CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(_CACHE_PATH), check_same_thread=False)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS translations (
            key TEXT PRIMARY KEY,
            translated TEXT NOT NULL,
            created_at REAL DEFAULT (strftime('%s', 'now'))
        )
        """
    )
    return conn


_conn = _connect()


def _make_key(
    translator: str,
    source: str,
    target: str,
    model: str,
    text: str,
) -> str:
    payload = f"{translator}\x1f{source}\x1f{target}\x1f{model}\x1f{text}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def get(
    translator: str,
    source: str,
    target: str,
    model: str,
    text: str,
) -> Optional[str]:
    key = _make_key(translator, source, target, model, text)
    with _lock:
        row = _conn.execute(
            "SELECT translated FROM translations WHERE key = ?", (key,)
        ).fetchone()
    return row[0] if row else None


def put(
    translator: str,
    source: str,
    target: str,
    model: str,
    text: str,
    translated: str,
) -> None:
    key = _make_key(translator, source, target, model, text)
    with _lock:
        _conn.execute(
            "INSERT OR REPLACE INTO translations (key, translated) "
            "VALUES (?, ?)",
            (key, translated),
        )
        _conn.commit()
