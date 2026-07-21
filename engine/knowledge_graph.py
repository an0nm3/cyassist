"""Phase F3: Knowledge Graph — unified queryable graph of all intelligence.

Unifies 14 siloed data sources across Rudra + Cyassist into a single
graph with typed nodes and labeled edges. All other components query
this graph instead of doing isolated DB lookups.

Node types (16):
  Technology, Framework, CVE, Exploit, Sink,
  Finding, Surface, Chain, Program, Policy,
  Detector, Probe, HistoricalReport, Evidence,
  PayloadVector, Session

Edge types (20):
  AFFECTS, HAS_EXPLOIT, TARGETS_SINK, FOUND_ON,
  HAS_EVIDENCE, USES_SINK, PART_OF_CHAIN, HAS_POLICY,
  HAS_FINDING, DETECTS, RELATED_TO, RUNS_ON,
  TESTED_WITH, HAS_CVE, SIMILAR_TO, LEADS_TO,
  BLOCKED_BY, REQUIRES_AUTH, PRODUCES, DEPENDS_ON

Usage:
    kg = KnowledgeGraph()
    kg.populate_all()  # Import from all existing stores
    techs = kg.query_nodes("Technology")
    cves = kg.find_related("Technology:laravel", "CVE")
"""

import json
import logging
import sqlite3
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger("knowledge_graph")

# ── Node Types ─────────────────────────────────────────────────────────

NODE_TECHNOLOGY = "Technology"
NODE_FRAMEWORK = "Framework"
NODE_CVE = "CVE"
NODE_EXPLOIT = "Exploit"
NODE_SINK = "Sink"
NODE_FINDING = "Finding"
NODE_SURFACE = "Surface"
NODE_CHAIN = "Chain"
NODE_PROGRAM = "Program"
NODE_POLICY = "Policy"
NODE_DETECTOR = "Detector"
NODE_PROBE = "Probe"
NODE_HISTORICAL_REPORT = "HistoricalReport"
NODE_EVIDENCE = "Evidence"
NODE_PAYLOAD_VECTOR = "PayloadVector"
NODE_SESSION = "Session"

ALL_NODE_TYPES = frozenset({
    NODE_TECHNOLOGY, NODE_FRAMEWORK, NODE_CVE, NODE_EXPLOIT,
    NODE_SINK, NODE_FINDING, NODE_SURFACE, NODE_CHAIN,
    NODE_PROGRAM, NODE_POLICY, NODE_DETECTOR, NODE_PROBE,
    NODE_HISTORICAL_REPORT, NODE_EVIDENCE, NODE_PAYLOAD_VECTOR,
    NODE_SESSION,
})

# ── Edge Types ─────────────────────────────────────────────────────────

EDGE_AFFECTS = "AFFECTS"                     # CVE → Technology
EDGE_HAS_EXPLOIT = "HAS_EXPLOIT"             # CVE → Exploit
EDGE_TARGETS_SINK = "TARGETS_SINK"           # Exploit → Sink
EDGE_FOUND_ON = "FOUND_ON"                   # Finding → Surface
EDGE_HAS_EVIDENCE = "HAS_EVIDENCE"           # Finding → Evidence
EDGE_USES_SINK = "USES_SINK"                 # Finding → Sink
EDGE_PART_OF_CHAIN = "PART_OF_CHAIN"         # Finding → Chain
EDGE_HAS_POLICY = "HAS_POLICY"               # Program → Policy
EDGE_HAS_FINDING = "HAS_FINDING"             # Program → Finding
EDGE_DETECTS = "DETECTS"                     # Detector → Sink
EDGE_RELATED_TO = "RELATED_TO"               # Finding → Technology
EDGE_RUNS_ON = "RUNS_ON"                     # Surface → Technology
EDGE_TESTED_WITH = "TESTED_WITH"             # Surface → Probe
EDGE_HAS_CVE = "HAS_CVE"                     # Technology → CVE
EDGE_SIMILAR_TO = "SIMILAR_TO"               # Finding → Finding
EDGE_LEADS_TO = "LEADS_TO"                   # Surface → Surface
EDGE_BLOCKED_BY = "BLOCKED_BY"               # Probe → Policy
EDGE_REQUIRES_AUTH = "REQUIRES_AUTH"         # Surface → Session
EDGE_PRODUCES = "PRODUCES"                   # Detector → Finding
EDGE_DEPENDS_ON = "DEPENDS_ON"               # Framework → Technology

ALL_EDGE_TYPES = frozenset({
    EDGE_AFFECTS, EDGE_HAS_EXPLOIT, EDGE_TARGETS_SINK,
    EDGE_FOUND_ON, EDGE_HAS_EVIDENCE, EDGE_USES_SINK,
    EDGE_PART_OF_CHAIN, EDGE_HAS_POLICY, EDGE_HAS_FINDING,
    EDGE_DETECTS, EDGE_RELATED_TO, EDGE_RUNS_ON, EDGE_TESTED_WITH,
    EDGE_HAS_CVE, EDGE_SIMILAR_TO, EDGE_LEADS_TO, EDGE_BLOCKED_BY,
    EDGE_REQUIRES_AUTH, EDGE_PRODUCES, EDGE_DEPENDS_ON,
})


@dataclass
class Node:
    """A single node in the knowledge graph."""
    node_type: str
    name: str
    properties: dict = field(default_factory=dict)

    def uid(self) -> str:
        """Unique ID string: '{type}:{name}'"""
        return f"{self.node_type}:{self.name}"


@dataclass
class Edge:
    """A labeled edge between two nodes."""
    source: str        # uid of source node
    target: str        # uid of target node
    edge_type: str
    properties: dict = field(default_factory=dict)
    confidence: float = 1.0


class KnowledgeGraph:
    """Unified graph store backed by SQLite adjacency list.

    Schema:
      nodes:  (id TEXT PK, type TEXT, name TEXT, properties JSON,
               created_at TEXT, updated_at TEXT)
      edges:  (id INTEGER PK, source_id TEXT, target_id TEXT,
               type TEXT, properties JSON, confidence REAL,
               created_at TEXT)
      indexes on (type, name), (source_id, type), (target_id, type)

    Thread-safe: uses WAL + check_same_thread=False.
    """

    def __init__(self, db_path: str = ""):
        if not db_path:
            db_path = str(Path.home() / ".local" / "share" / "cyassist" / "knowledge_graph.db")
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[sqlite3.Connection] = None
        self._populated = False

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA synchronous=NORMAL")
            self._conn.execute("PRAGMA foreign_keys=ON")
            self._init_schema()
        return self._conn

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    # ── Node CRUD ─────────────────────────────────────────────────────

    def add_node(self, node: Node, commit: bool = True) -> str:
        """Add a node. Returns its UID. Updates updated_at if exists."""
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        uid = node.uid()
        props = json.dumps(node.properties)
        self.conn.execute(
            """INSERT INTO nodes (id, type, name, properties, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?)
               ON CONFLICT(id) DO UPDATE SET
                   properties = excluded.properties,
                   updated_at = excluded.updated_at""",
            (uid, node.node_type, node.name, props, now, now),
        )
        if commit:
            self.conn.commit()
        return uid

    def add_node_batch(self, nodes: list[Node], commit: bool = True) -> int:
        """Batch insert nodes. Returns count."""
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        rows = []
        for n in nodes:
            uid = n.uid()
            props = json.dumps(n.properties)
            rows.append((uid, n.node_type, n.name, props, now, now))
        self.conn.executemany(
            """INSERT OR REPLACE INTO nodes (id, type, name, properties, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            rows,
        )
        if commit:
            self.conn.commit()
        return len(rows)

    def get_node(self, uid: str) -> Optional[Node]:
        """Get a node by UID."""
        row = self.conn.execute("SELECT * FROM nodes WHERE id = ?", (uid,)).fetchone()
        if row is None:
            return None
        return Node(
            node_type=row["type"],
            name=row["name"],
            properties=json.loads(row["properties"]),
        )

    def get_node_by_type_name(self, node_type: str, name: str) -> Optional[Node]:
        return self.get_node(f"{node_type}:{name}")

    def query_nodes(
        self,
        node_type: Optional[str] = None,
        property_filter: Optional[dict] = None,
        limit: int = 100,
    ) -> list[Node]:
        """Query nodes by type and optional property filter."""
        conditions = []
        params: dict = {}

        if node_type:
            conditions.append("type = :type")
            params["type"] = node_type

        if property_filter:
            for k, v in property_filter.items():
                conditions.append(f"json_extract(properties, '$.{k}') = :prop_{k}")
                params[f"prop_{k}"] = json.dumps(v) if isinstance(v, (list, dict)) else v

        where = " AND ".join(conditions) if conditions else "1=1"
        params["limit"] = limit
        rows = self.conn.execute(
            f"SELECT * FROM nodes WHERE {where} ORDER BY created_at DESC LIMIT :limit",
            params,
        ).fetchall()
        return [
            Node(node_type=r["type"], name=r["name"], properties=json.loads(r["properties"]))
            for r in rows
        ]

    def count_nodes(self, node_type: Optional[str] = None) -> int:
        if node_type:
            row = self.conn.execute("SELECT COUNT(*) as c FROM nodes WHERE type = ?", (node_type,)).fetchone()
        else:
            row = self.conn.execute("SELECT COUNT(*) as c FROM nodes").fetchone()
        return row["c"] if row else 0

    # ── Edge CRUD ─────────────────────────────────────────────────────

    def add_edge(self, edge: Edge, commit: bool = True) -> bool:
        """Add an edge. Returns True if new."""
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        props = json.dumps(edge.properties)
        try:
            self.conn.execute(
                """INSERT OR IGNORE INTO edges
                   (source_id, target_id, type, properties, confidence, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (edge.source, edge.target, edge.edge_type, props, edge.confidence, now),
            )
            if commit:
                self.conn.commit()
            return True
        except Exception:
            return False

    def add_edge_batch(self, edges: list[Edge], commit: bool = True) -> int:
        """Batch insert edges. Returns count."""
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        rows = []
        for e in edges:
            props = json.dumps(e.properties)
            rows.append((e.source, e.target, e.edge_type, props, e.confidence, now))
        count = 0
        for row in rows:
            try:
                self.conn.execute(
                    """INSERT OR IGNORE INTO edges
                       (source_id, target_id, type, properties, confidence, created_at)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    row,
                )
                count += 1
            except Exception:
                pass
        if commit:
            self.conn.commit()
        return count

    def find_related(
        self,
        source_uid: str,
        target_type: Optional[str] = None,
        edge_type: Optional[str] = None,
        max_depth: int = 1,
    ) -> list[tuple[Node, str]]:
        """Find nodes related to a source node via edges.

        Returns list of (Node, edge_type) tuples.
        Supports transitive traversal via max_depth > 1 (recursive CTE).
        """
        if max_depth == 1:
            conditions = ["e.source_id = :source"]
            params: dict = {"source": source_uid}

            if target_type:
                conditions.append("n.type = :target_type")
                params["target_type"] = target_type
            if edge_type:
                conditions.append("e.type = :edge_type")
                params["edge_type"] = edge_type

            where = " AND ".join(conditions)
            rows = self.conn.execute(
                f"""SELECT n.id, n.type, n.name, n.properties, e.type as edge_type
                    FROM edges e
                    JOIN nodes n ON n.id = e.target_id
                    WHERE {where}
                    ORDER BY e.confidence DESC""",
                params,
            ).fetchall()
            return [
                (Node(node_type=r["type"], name=r["name"], properties=json.loads(r["properties"])), r["edge_type"])
                for r in rows
            ]

        # Transitive traversal via recursive CTE
        rows = self.conn.execute(
            """WITH RECURSIVE
                traverse(source_id, target_id, type, depth, path) AS (
                    SELECT e.source_id, e.target_id, e.type, 1,
                           '[' || e.source_id || '->' || e.target_id || ']'
                    FROM edges e
                    WHERE e.source_id = ?
                    UNION ALL
                    SELECT e.source_id, e.target_id, e.type, t.depth + 1,
                           t.path || '[' || e.source_id || '->' || e.target_id || ']'
                    FROM edges e
                    JOIN traverse t ON t.target_id = e.source_id
                    WHERE t.depth < ?
                )
                SELECT DISTINCT n.id, n.type, n.name, n.properties, t.type as edge_type
                FROM traverse t
                JOIN nodes n ON n.id = t.target_id
                WHERE (? IS NULL OR n.type = ?)
                ORDER BY t.depth""",
            (source_uid, max_depth, target_type, target_type),
        ).fetchall()
        return [
            (Node(node_type=r["type"], name=r["name"], properties=json.loads(r["properties"])), r["edge_type"])
            for r in rows
        ]

    def find_parents(
        self,
        target_uid: str,
        source_type: Optional[str] = None,
        edge_type: Optional[str] = None,
    ) -> list[tuple[Node, str]]:
        """Find nodes that point TO this node via edges (reverse traversal)."""
        conditions = ["e.target_id = :target"]
        params: dict = {"target": target_uid}

        if source_type:
            conditions.append("n.type = :source_type")
            params["source_type"] = source_type
        if edge_type:
            conditions.append("e.type = :edge_type")
            params["edge_type"] = edge_type

        where = " AND ".join(conditions)
        rows = self.conn.execute(
            f"""SELECT n.id, n.type, n.name, n.properties, e.type as edge_type
                FROM edges e
                JOIN nodes n ON n.id = e.source_id
                WHERE {where}
                ORDER BY e.confidence DESC""",
            params,
        ).fetchall()
        return [
            (Node(node_type=r["type"], name=r["name"], properties=json.loads(r["properties"])), r["edge_type"])
            for r in rows
        ]

    def find_path(self, source_uid: str, target_uid: str, max_depth: int = 5) -> list[list[str]]:
        """Find all paths between two nodes up to max_depth."""
        rows = self.conn.execute(
            """WITH RECURSIVE
                paths(start_id, end_id, depth, path_str, last_id) AS (
                    SELECT e.source_id, e.target_id, 1,
                           '[' || e.source_id || ']' || '->[' || e.target_id || ']',
                           e.target_id
                    FROM edges e
                    WHERE e.source_id = ?
                    UNION ALL
                    SELECT p.start_id, e.target_id, p.depth + 1,
                           p.path_str || '->[' || e.target_id || ']',
                           e.target_id
                    FROM edges e
                    JOIN paths p ON p.last_id = e.source_id
                    WHERE p.depth < ? AND e.target_id != p.start_id
                )
                SELECT path_str FROM paths
                WHERE end_id = ?
                ORDER BY depth
                LIMIT 20""",
            (source_uid, max_depth, target_uid),
        ).fetchall()
        return [r["path_str"] for r in rows]

    def count_edges(self, edge_type: Optional[str] = None) -> int:
        if edge_type:
            row = self.conn.execute("SELECT COUNT(*) as c FROM edges WHERE type = ?", (edge_type,)).fetchone()
        else:
            row = self.conn.execute("SELECT COUNT(*) as c FROM edges").fetchone()
        return row["c"] if row else 0

    # ── Stats ──────────────────────────────────────────────────────────

    def stats(self) -> dict:
        return {
            "total_nodes": self.count_nodes(),
            "total_edges": self.count_edges(),
            "nodes_by_type": {
                r["type"]: r["c"]
                for r in self.conn.execute(
                    "SELECT type, COUNT(*) as c FROM nodes GROUP BY type ORDER BY c DESC"
                ).fetchall()
            },
            "edges_by_type": {
                r["type"]: r["c"]
                for r in self.conn.execute(
                    "SELECT type, COUNT(*) as c FROM edges GROUP BY type ORDER BY c DESC"
                ).fetchall()
            },
            "size_bytes": self.db_path.stat().st_size if self.db_path.exists() else 0,
            "populated": self._populated,
        }

    # ── Population ──────────────────────────────────────────────────────

    def populate_from_intel_db(self, db_path: str = ""):
        """Import nodes from Cyassist intel.db (cves, exploits, tech_cve)."""
        if not db_path:
            db_path = str(Path.home() / ".local" / "share" / "cyassist" / "intel.db")

        src = Path(db_path)
        if not src.exists():
            logger.warning("intel.db not found at %s", db_path)
            return 0

        count = 0
        conn = sqlite3.connect(str(src), check_same_thread=False)
        conn.row_factory = sqlite3.Row

        # CVE nodes
        try:
            for row in conn.execute("SELECT * FROM cves").fetchall():
                row = dict(row)
                cve_id = row.pop("id", "")
                if not cve_id:
                    continue
                row.pop("epss_percentile", None)
                self.add_node(Node(NODE_CVE, cve_id, row), commit=False)
                count += 1
        except Exception as e:
            logger.warning("Failed to import cves: %s", e)

        # Technology → CVE edges
        try:
            for row in conn.execute("SELECT * FROM tech_cve").fetchall():
                row = dict(row)
                tech = str(row.get("technology") or "")
                cve_id = str(row.get("cve_id") or "")
                if tech and cve_id:
                    self.add_node(Node(NODE_TECHNOLOGY, tech, {}), commit=False)
                    self.add_edge(Edge(
                        source=f"{NODE_CVE}:{cve_id}",
                        target=f"{NODE_TECHNOLOGY}:{tech}",
                        edge_type=EDGE_AFFECTS,
                        properties={
                            "version_range": str(row.get("version_range") or ""),
                            "sink_type": str(row.get("sink_type") or ""),
                        },
                    ), commit=False)
                    count += 1
        except Exception as e:
            logger.warning("Failed to import tech_cve: %s", e)

        # Exploit nodes
        try:
            for row in conn.execute("SELECT * FROM exploits").fetchall():
                row = dict(row)
                cve_id = row.pop("cve_id", "")
                source = row.pop("source", "")
                title = row.pop("title", "")
                exploit_id = f"{source}:{title}"[:100]
                if not exploit_id.strip(":"):
                    continue
                self.add_node(Node(NODE_EXPLOIT, exploit_id, row), commit=False)
                if cve_id:
                    self.add_edge(Edge(
                        source=f"{NODE_CVE}:{cve_id}",
                        target=f"{NODE_EXPLOIT}:{exploit_id}",
                        edge_type=EDGE_HAS_EXPLOIT,
                        properties={"source": source},
                    ), commit=False)
                sink = row.get("sink_type", "")
                if sink:
                    self.add_node(Node(NODE_SINK, sink, {}), commit=False)
                    self.add_edge(Edge(
                        source=f"{NODE_EXPLOIT}:{exploit_id}",
                        target=f"{NODE_SINK}:{sink}",
                        edge_type=EDGE_TARGETS_SINK,
                    ), commit=False)
                count += 1
        except Exception as e:
            logger.warning("Failed to import exploits: %s", e)

        conn.close()
        self.conn.commit()
        logger.info("Imported %d nodes/edges from intel.db", count)
        return count

    def populate_from_vectors_db(self, db_path: str = ""):
        """Import PayloadVector nodes from vectors.db."""
        if not db_path:
            db_path = str(Path.home() / ".local" / "share" / "cyassist" / "vectors.db")

        src = Path(db_path)
        if not src.exists():
            logger.warning("vectors.db not found at %s", db_path)
            return 0

        count = 0
        conn = sqlite3.connect(str(src), check_same_thread=False)
        conn.row_factory = sqlite3.Row

        try:
            for row in conn.execute("SELECT * FROM feature_vectors").fetchall():
                row = dict(row)
                payload_hash = str(row.pop("payload_hash", ""))
                if not payload_hash:
                    continue
                row.pop("id", None)
                self.add_node(Node(NODE_PAYLOAD_VECTOR, payload_hash, row), commit=False)
                count += 1
        except Exception as e:
            logger.warning("Failed to import vectors: %s", e)

        conn.close()
        self.conn.commit()
        logger.info("Imported %d PayloadVector nodes", count)
        return count

    def populate_all(self, intel_db: str = "", vectors_db: str = ""):
        """Import from all existing stores."""
        logger.info("Populating knowledge graph...")
        self._populated = True
        total = 0
        total += self.populate_from_intel_db(intel_db)
        total += self.populate_from_vectors_db(vectors_db)
        logger.info("Knowledge graph populated: %d total nodes/edges", total)
        return total

    def _init_schema(self):
        """Initialize schema, gracefully handling existing data."""
        cur = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='nodes'")
        tables_exist = cur.fetchone() is not None

        if not tables_exist:
            self.conn.executescript("""
                CREATE TABLE nodes (
                    id TEXT PRIMARY KEY,
                    type TEXT NOT NULL,
                    name TEXT NOT NULL,
                    properties TEXT NOT NULL DEFAULT '{}',
                    created_at TEXT NOT NULL DEFAULT '',
                    updated_at TEXT NOT NULL DEFAULT ''
                );
                CREATE INDEX idx_nodes_type ON nodes(type);
                CREATE INDEX idx_nodes_name ON nodes(name);
                CREATE UNIQUE INDEX idx_nodes_type_name ON nodes(type, name);

                CREATE TABLE edges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_id TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    type TEXT NOT NULL,
                    properties TEXT NOT NULL DEFAULT '{}',
                    confidence REAL NOT NULL DEFAULT 1.0,
                    created_at TEXT NOT NULL DEFAULT '',
                    FOREIGN KEY (source_id) REFERENCES nodes(id),
                    FOREIGN KEY (target_id) REFERENCES nodes(id)
                );
                CREATE UNIQUE INDEX idx_edges_unique ON edges(source_id, target_id, type);
                CREATE INDEX idx_edges_source ON edges(source_id);
                CREATE INDEX idx_edges_target ON edges(target_id);
                CREATE INDEX idx_edges_type ON edges(type);
                CREATE INDEX idx_edges_source_type ON edges(source_id, type);
                CREATE INDEX idx_edges_target_type ON edges(target_id, type);
            """)

        # Ensure unique edge index exists (may have been dropped)
        try:
            self.conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_edges_unique ON edges(source_id, target_id, type)")
        except Exception:
            pass

    def clear(self):
        """Delete the DB file for a clean re-population."""
        if self._conn:
            self._conn.close()
            self._conn = None
        if self.db_path.exists():
            self.db_path.unlink()
        self._populated = False

    def size_bytes(self) -> int:
        return self.db_path.stat().st_size if self.db_path.exists() else 0


# ── Standalone Helpers ────────────────────────────────────────────────


def make_technology_node(name: str, confidence: float = 0.5, signals: Optional[list[str]] = None) -> Node:
    return Node(NODE_TECHNOLOGY, name, {
        "confidence": confidence,
        "signals": signals or [],
        "first_seen": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    })


def make_finding_node(finding_id: str, sink: str, severity: str = "medium", confidence: float = 0.5, **extra) -> Node:
    return Node(NODE_FINDING, finding_id, {
        "sink": sink,
        "severity": severity,
        "confidence": confidence,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        **extra,
    })


def make_surface_node(path: str, method: str = "GET", requires_auth: bool = False, **extra) -> Node:
    return Node(NODE_SURFACE, f"{method}:{path}", {
        "path": path,
        "method": method,
        "requires_auth": requires_auth,
        **extra,
    })
