#!/usr/bin/env python3
"""Cyassist Intel DB — SQLite store for the news archive.
Stores metadata + URLs only. Target: <10MB."""

import datetime
import json
import sqlite3
import time
from pathlib import Path
from typing import Optional

DB_PATH = Path.home() / ".local" / "share" / "cyassist" / "intel.db"


def get_db(path=None) -> sqlite3.Connection:
    p = Path(path) if path else DB_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(p))
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA page_size=4096")
    return db


def init(db=None):
    if db is None:
        db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS news (
            id TEXT PRIMARY KEY,
            source TEXT,
            url TEXT UNIQUE,
            title TEXT,
            date TEXT,
            tags TEXT,
            cve_refs TEXT,
            body_snippet TEXT,
            india_relevant INTEGER DEFAULT 0,
            fetched_at TEXT
        );

        CREATE TABLE IF NOT EXISTS news_sources (
            name TEXT PRIMARY KEY,
            url TEXT,
            type TEXT DEFAULT 'rss',
            enabled INTEGER DEFAULT 1,
            last_fetch TEXT,
            article_count INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS seen_ids (
            id TEXT PRIMARY KEY,
            source TEXT,
            seen_at TEXT
        );
    """)
    db.commit()


class IntelDB:
    def __init__(self, path=None):
        self.db = get_db(path)
        init(self.db)

    def close(self):
        self.db.close()

    def size_mb(self) -> float:
        p = Path(self.db.execute("PRAGMA database_list").fetchone()[2])
        return p.stat().st_size / (1024 * 1024) if p.exists() else 0

    # ── News ──
    def add_news(self, source: str, url: str, title: str, date_str: str = None,
                 tags: list = None, cve_refs: list = None, body_snippet: str = "",
                 india_relevant: bool = False) -> bool:
        import hashlib
        key = hashlib.sha256(url.encode()).hexdigest()[:16]
        try:
            self.db.execute("""
                INSERT INTO news (id, source, url, title, date, tags, cve_refs,
                    body_snippet, india_relevant, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (key, source, url, title, date_str or datetime.datetime.now().strftime("%Y-%m-%d"),
                  json.dumps(tags or []), json.dumps(cve_refs or []),
                  body_snippet[:500], 1 if india_relevant else 0,
                  datetime.datetime.now().isoformat()))
            self.db.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def search_news(self, query: str = "", source: str = "", days: int = 0,
                    india_only: bool = False, limit: int = 50) -> list[dict]:
        sql = "SELECT * FROM news WHERE 1=1"
        params = []
        if query:
            sql += " AND (title LIKE ? OR body_snippet LIKE ? OR tags LIKE ?)"
            params += [f"%{query}%", f"%{query}%", f"%{query}%"]
        if source:
            sql += " AND source LIKE ?"
            params += [f"%{source}%"]
        if days > 0:
            cutoff = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
            sql += " AND date >= ?"
            params += [cutoff]
        if india_only:
            sql += " AND india_relevant = 1"
        sql += " ORDER BY date DESC LIMIT ?"
        params += [limit]
        return [dict(r) for r in self.db.execute(sql, params).fetchall()]

    # ── Seen IDs (dedup) ──
    def is_seen(self, id_str: str, source: str = "") -> bool:
        return self.db.execute(
            "SELECT 1 FROM seen_ids WHERE id=?", (id_str,)).fetchone() is not None

    def mark_seen(self, id_str: str, source: str = ""):
        self.db.execute("INSERT OR IGNORE INTO seen_ids (id, source, seen_at) VALUES (?, ?, ?)",
                        (id_str, source, datetime.datetime.now().isoformat()))
        self.db.commit()

    # ── Stats ──
    def stats(self) -> dict:
        counts = {}
        for t in ["news", "news_sources", "seen_ids"]:
            r = self.db.execute(f"SELECT COUNT(*) as c FROM {t}").fetchone()
            counts[t] = r["c"]
        return {"size_mb": round(self.size_mb(), 3), **counts}


if __name__ == "__main__":
    db = IntelDB()
    print(json.dumps(db.stats(), indent=2))
    db.close()
