#!/usr/bin/env python3
"""Cyassist Intel DB — single SQLite store for all structured intel.
Stores metadata + URLs only. No blobs. Target: <10MB for 100K entries."""

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
        CREATE TABLE IF NOT EXISTS cves (
            id TEXT PRIMARY KEY,
            cvss REAL,
            severity TEXT,
            epss REAL,
            epss_percentile REAL,
            description TEXT,
            cwes TEXT,
            vector TEXT,
            techniques TEXT,
            in_kev INTEGER DEFAULT 0,
            has_poc INTEGER DEFAULT 0,
            updated_at TEXT
        );

        CREATE TABLE IF NOT EXISTS exploits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cve_id TEXT REFERENCES cves(id),
            source TEXT,
            title TEXT,
            url TEXT UNIQUE,
            technique TEXT,
            sink_type TEXT,
            parameter_template TEXT,
            payload_template TEXT,
            target_software TEXT,
            version_range TEXT,
            tags TEXT,
            date TEXT,
            UNIQUE(url)
        );

        CREATE INDEX IF NOT EXISTS idx_exploits_cve ON exploits(cve_id);

        CREATE TABLE IF NOT EXISTS templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cve_id TEXT,
            template_id TEXT,
            template_name TEXT,
            severity TEXT,
            technique TEXT,
            tags TEXT,
            nuclei_cmd TEXT,
            url TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_templates_cve ON templates(cve_id);

        CREATE TABLE IF NOT EXISTS tech_cve (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            technology TEXT,
            cve_id TEXT,
            version_range TEXT,
            sink_type TEXT,
            technique TEXT,
            source TEXT,
            UNIQUE(technology, cve_id)
        );

        CREATE INDEX IF NOT EXISTS idx_tech_cve_tech ON tech_cve(technology);

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

        CREATE TABLE IF NOT EXISTS targets (
            name TEXT PRIMARY KEY,
            url TEXT,
            techs TEXT,
            keywords TEXT,
            updated_at TEXT
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

    # ── CVEs ──
    def upsert_cve(self, cve_id: str, **kw):
        fields = {
            "cvss": kw.get("cvss"), "severity": kw.get("severity"),
            "epss": kw.get("epss", 0), "epss_percentile": kw.get("epss_percentile", 0),
            "description": kw.get("description", ""),
            "cwes": json.dumps(kw.get("cwes", [])),
            "vector": kw.get("vector", ""),
            "techniques": json.dumps(kw.get("techniques", [])),
            "in_kev": 1 if kw.get("in_kev") else 0,
            "has_poc": 1 if kw.get("has_poc") else 0,
            "updated_at": datetime.datetime.now().isoformat(),
        }
        cols = ", ".join(field for field in fields)
        placeholders = ", ".join(f":{field}" for field in fields)
        update = ", ".join(f"{field}=excluded.{field}" for field in fields)
        self.db.execute(
            f"INSERT INTO cves (id, {cols}) VALUES (:id, {placeholders}) "
            f"ON CONFLICT(id) DO UPDATE SET {update}",
            {"id": cve_id, **{k: v for k, v in fields.items() if v is not None}}
        )
        self.db.commit()

    def get_cve(self, cve_id: str) -> Optional[dict]:
        row = self.db.execute("SELECT * FROM cves WHERE id=?", (cve_id,)).fetchone()
        if row:
            d = dict(row)
            d["cwes"] = json.loads(d.get("cwes") or "[]")
            d["techniques"] = json.loads(d.get("techniques") or "[]")
            return d
        return None

    def search_cves(self, query: str = "", technique: str = "", min_cvss: float = 0, limit: int = 50) -> list[dict]:
        sql = "SELECT * FROM cves WHERE 1=1"
        params = []
        if query:
            sql += " AND (id LIKE ? OR description LIKE ?)"
            params += [f"%{query}%", f"%{query}%"]
        if technique:
            sql += " AND techniques LIKE ?"
            params += [f"%{technique}%"]
        if min_cvss:
            sql += " AND cvss >= ?"
            params += [min_cvss]
        sql += " ORDER BY cvss DESC NULLS LAST LIMIT ?"
        params += [limit]
        return [dict(r) for r in self.db.execute(sql, params).fetchall()]

    def get_cves_by_tech(self, technology: str) -> list[dict]:
        rows = self.db.execute(
            "SELECT c.* FROM cves c JOIN tech_cve t ON c.id = t.cve_id WHERE t.technology=?",
            (technology.lower(),)
        ).fetchall()
        return [dict(r) for r in rows]

    # ── Exploits (DNA) ──
    def add_exploit(self, cve_id: str, source: str, title: str, url: str,
                    technique: str = "", sink_type: str = "",
                    parameter_template: str = "", payload_template: str = "",
                    target_software: str = "", version_range: str = "",
                    tags: list = None):
        try:
            self.db.execute("""
                INSERT INTO exploits (cve_id, source, title, url, technique, sink_type,
                    parameter_template, payload_template, target_software, version_range, tags, date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (cve_id, source, title, url, technique, sink_type,
                  parameter_template, payload_template, target_software, version_range,
                  json.dumps(tags or []), datetime.datetime.now().strftime("%Y-%m-%d")))
            self.db.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_exploits_for_cve(self, cve_id: str) -> list[dict]:
        return [dict(r) for r in self.db.execute(
            "SELECT * FROM exploits WHERE cve_id=?", (cve_id,)).fetchall()]

    def get_exploits_by_technique(self, technique: str, limit: int = 20) -> list[dict]:
        return [dict(r) for r in self.db.execute(
            "SELECT * FROM exploits WHERE technique LIKE ? LIMIT ?",
            (f"%{technique}%", limit)).fetchall()]

    # ── Technology→CVE mapping ──
    def add_tech_cve(self, technology: str, cve_id: str, version_range: str = "",
                     sink_type: str = "", technique: str = "", source: str = ""):
        try:
            self.db.execute("""
                INSERT INTO tech_cve (technology, cve_id, version_range, sink_type, technique, source)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (technology.lower(), cve_id, version_range, sink_type, technique, source))
            self.db.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_tech_cves(self, technology: str) -> list[dict]:
        return [dict(r) for r in self.db.execute(
            "SELECT * FROM tech_cve WHERE technology=?", (technology.lower(),)).fetchall()]

    def search_tech(self, query: str) -> list[str]:
        rows = self.db.execute(
            "SELECT DISTINCT technology FROM tech_cve WHERE technology LIKE ? LIMIT 50",
            (f"%{query.lower()}%",)
        ).fetchall()
        return [r["technology"] for r in rows]

    def get_sink_for_technique(self, technique: str) -> str:
        mapping = {
            "xss": "reflected_xss", "sqli": "sql_injection", "ssrf": "ssrf",
            "rce": "command_injection", "lfi": "lfi", "ssti": "ssti",
            "idor": "idor", "open-redirect": "open_redirect",
            "prototype-pollution": "prototype_pollution",
            "race-condition": "race_condition",
            "oauth": "oauth_misconfig", "jwt": "jwt_attack",
            "xxe": "xxe", "file-upload": "file_upload",
            "nosqli": "nosqli", "csrf": "csrf_misconfig",
            "path-traversal": "path_traversal",
        }
        return mapping.get(technique.lower().replace(" ", "-"), "generic")

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

    # ── Templates index ──
    def add_template(self, cve_id: str, template_id: str, template_name: str = "",
                     severity: str = "", technique: str = "", tags: list = None,
                     nuclei_cmd: str = "", url: str = ""):
        try:
            self.db.execute("""
                INSERT INTO templates (cve_id, template_id, template_name, severity,
                    technique, tags, nuclei_cmd, url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (cve_id, template_id, template_name, severity, technique,
                  json.dumps(tags or []), nuclei_cmd, url))
            self.db.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_templates_for_cve(self, cve_id: str) -> list[dict]:
        return [dict(r) for r in self.db.execute(
            "SELECT * FROM templates WHERE cve_id=?", (cve_id,)).fetchall()]

    # ── Seen IDs (dedup) ──
    def is_seen(self, id_str: str, source: str = "") -> bool:
        return self.db.execute(
            "SELECT 1 FROM seen_ids WHERE id=?", (id_str,)).fetchone() is not None

    def mark_seen(self, id_str: str, source: str = ""):
        self.db.execute("INSERT OR IGNORE INTO seen_ids (id, source, seen_at) VALUES (?, ?, ?)",
                        (id_str, source, datetime.datetime.now().isoformat()))
        self.db.commit()

    # ── Targets ──
    def upsert_target(self, name: str, url: str = "", techs: list = None, keywords: list = None):
        self.db.execute("""
            INSERT INTO targets (name, url, techs, keywords, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                url=excluded.url, techs=excluded.techs,
                keywords=excluded.keywords, updated_at=excluded.updated_at
        """, (name, url, json.dumps(techs or []), json.dumps(keywords or []),
              datetime.datetime.now().isoformat()))
        self.db.commit()

    def get_targets(self) -> list[dict]:
        return [dict(r) for r in self.db.execute("SELECT * FROM targets").fetchall()]

    # ── Stats ──
    def stats(self) -> dict:
        tables = ["cves", "exploits", "templates", "tech_cve", "news", "targets"]
        counts = {}
        for t in tables:
            r = self.db.execute(f"SELECT COUNT(*) as c FROM {t}").fetchone()
            counts[t] = r["c"]
        return {"size_mb": round(self.size_mb(), 3), **counts}


if __name__ == "__main__":
    db = IntelDB()
    print(json.dumps(db.stats(), indent=2))
    db.close()
