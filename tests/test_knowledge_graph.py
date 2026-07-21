"""Tests for Phase F3: Knowledge Graph."""
import json
import os
import tempfile

import pytest

from engine.knowledge_graph import (
    KnowledgeGraph,
    Node,
    Edge,
    NODE_TECHNOLOGY,
    NODE_CVE,
    NODE_SINK,
    NODE_EXPLOIT,
    NODE_FINDING,
    NODE_SURFACE,
    NODE_PAYLOAD_VECTOR,
    EDGE_AFFECTS,
    EDGE_HAS_EXPLOIT,
    EDGE_TARGETS_SINK,
    EDGE_FOUND_ON,
    EDGE_RUNS_ON,
    EDGE_USES_SINK,
)


@pytest.fixture
def kg():
    """Create a clean knowledge graph in a temp file."""
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    g = KnowledgeGraph(tmp.name)
    yield g
    g.close()
    os.unlink(tmp.name)


class TestNodeCRUD:
    def test_add_node(self, kg):
        uid = kg.add_node(Node(NODE_TECHNOLOGY, "laravel", {"confidence": 0.9}))
        assert uid == "Technology:laravel"
        assert kg.count_nodes() == 1

    def test_get_node(self, kg):
        kg.add_node(Node(NODE_TECHNOLOGY, "nginx", {"version": "1.18"}))
        node = kg.get_node("Technology:nginx")
        assert node is not None
        assert node.name == "nginx"
        assert node.node_type == NODE_TECHNOLOGY
        assert node.properties["version"] == "1.18"

    def test_get_nonexistent_node(self, kg):
        assert kg.get_node("Technology:nonexistent") is None

    def test_get_node_by_type_name(self, kg):
        kg.add_node(Node(NODE_CVE, "CVE-2021-3129", {"cvss": 9.1}))
        node = kg.get_node_by_type_name(NODE_CVE, "CVE-2021-3129")
        assert node is not None
        assert node.properties["cvss"] == 9.1

    def test_add_node_batch(self, kg):
        nodes = [
            Node(NODE_TECHNOLOGY, "php"),
            Node(NODE_TECHNOLOGY, "python"),
            Node(NODE_TECHNOLOGY, "java"),
        ]
        count = kg.add_node_batch(nodes)
        assert count == 3
        assert kg.count_nodes(NODE_TECHNOLOGY) == 3

    def test_query_nodes_by_type(self, kg):
        kg.add_node_batch([
            Node(NODE_TECHNOLOGY, "react"),
            Node(NODE_TECHNOLOGY, "vue"),
            Node(NODE_CVE, "CVE-2023-0", {"cvss": 7.5}),
        ])
        techs = kg.query_nodes(NODE_TECHNOLOGY)
        assert len(techs) == 2
        assert {t.name for t in techs} == {"react", "vue"}

    def test_query_nodes_with_property_filter(self, kg):
        kg.add_node_batch([
            Node(NODE_CVE, "CVE-1", {"cvss": 9.0, "severity": "critical"}),
            Node(NODE_CVE, "CVE-2", {"cvss": 5.0, "severity": "medium"}),
            Node(NODE_CVE, "CVE-3", {"cvss": 3.0, "severity": "low"}),
        ])
        results = kg.query_nodes(NODE_CVE, {"severity": "critical"})
        assert len(results) == 1
        assert results[0].name == "CVE-1"

    def test_duplicate_node_updates(self, kg):
        kg.add_node(Node(NODE_TECHNOLOGY, "react", {"version": "17.0"}))
        kg.add_node(Node(NODE_TECHNOLOGY, "react", {"version": "18.0"}))
        assert kg.count_nodes(NODE_TECHNOLOGY) == 1
        node = kg.get_node("Technology:react")
        assert node.properties["version"] == "18.0"


class TestEdgeCRUD:
    def test_add_edge(self, kg):
        kg.add_node(Node(NODE_CVE, "CVE-1"))
        kg.add_node(Node(NODE_TECHNOLOGY, "laravel"))
        added = kg.add_edge(Edge("CVE:CVE-1", "Technology:laravel", EDGE_AFFECTS))
        assert added
        assert kg.count_edges() == 1

    def test_duplicate_edge_ignored(self, kg):
        kg.add_node(Node(NODE_CVE, "CVE-1"))
        kg.add_node(Node(NODE_TECHNOLOGY, "laravel"))
        kg.add_edge(Edge("CVE:CVE-1", "Technology:laravel", EDGE_AFFECTS))
        kg.add_edge(Edge("CVE:CVE-1", "Technology:laravel", EDGE_AFFECTS))
        assert kg.count_edges() == 1

    def test_add_edge_batch(self, kg):
        kg.add_node_batch([
            Node(NODE_CVE, "CVE-1"),
            Node(NODE_CVE, "CVE-2"),
            Node(NODE_TECHNOLOGY, "laravel"),
            Node(NODE_TECHNOLOGY, "php"),
        ])
        edges = [
            Edge("CVE:CVE-1", "Technology:laravel", EDGE_AFFECTS),
            Edge("CVE:CVE-2", "Technology:php", EDGE_AFFECTS),
        ]
        count = kg.add_edge_batch(edges)
        assert count == 2

    def test_edge_properties(self, kg):
        kg.add_node(Node(NODE_CVE, "CVE-1"))
        kg.add_node(Node(NODE_TECHNOLOGY, "laravel"))
        kg.add_edge(Edge(
            "CVE:CVE-1", "Technology:laravel", EDGE_AFFECTS,
            {"version_range": "<=8.x", "sink_type": "debug_mode"},
            confidence=0.95,
        ))
        related = kg.find_related("CVE:CVE-1", NODE_TECHNOLOGY)
        assert len(related) == 1


class TestGraphQueries:
    def test_find_related_direct(self, kg):
        kg.add_node_batch([
            Node(NODE_CVE, "CVE-1"),
            Node(NODE_CVE, "CVE-2"),
            Node(NODE_TECHNOLOGY, "laravel"),
        ])
        kg.add_edge_batch([
            Edge("CVE:CVE-1", "Technology:laravel", EDGE_AFFECTS),
            Edge("CVE:CVE-2", "Technology:laravel", EDGE_AFFECTS),
        ])
        # Edges are CVE → Technology, so find_parents finds CVEs for a tech
        parents = kg.find_parents("Technology:laravel", NODE_CVE)
        assert len(parents) == 2
        assert {n.name for n, _ in parents} == {"CVE-1", "CVE-2"}

    def test_find_related_forward(self, kg):
        kg.add_node_batch([
            Node(NODE_EXPLOIT, "e1"),
            Node(NODE_EXPLOIT, "e2"),
            Node(NODE_CVE, "CVE-1"),
        ])
        kg.add_edge_batch([
            Edge("CVE:CVE-1", "Exploit:e1", EDGE_HAS_EXPLOIT),
            Edge("CVE:CVE-1", "Exploit:e2", EDGE_HAS_EXPLOIT),
        ])
        related = kg.find_related("CVE:CVE-1", NODE_EXPLOIT)
        assert len(related) == 2

    def test_find_related_with_edge_type(self, kg):
        kg.add_node_batch([
            Node(NODE_CVE, "CVE-1"),
            Node(NODE_EXPLOIT, "exploit-1"),
            Node(NODE_SINK, "sqli"),
        ])
        kg.add_edge_batch([
            Edge("CVE:CVE-1", "Exploit:exploit-1", EDGE_HAS_EXPLOIT),
            Edge("Exploit:exploit-1", "Sink:sqli", EDGE_TARGETS_SINK),
        ])
        related = kg.find_related("CVE:CVE-1", NODE_EXPLOIT, EDGE_HAS_EXPLOIT)
        assert len(related) == 1
        assert related[0][0].name == "exploit-1"

    def test_find_parents(self, kg):
        kg.add_node_batch([
            Node(NODE_CVE, "CVE-1"),
            Node(NODE_EXPLOIT, "exploit-1"),
            Node(NODE_SINK, "sqli"),
        ])
        kg.add_edge_batch([
            Edge("CVE:CVE-1", "Exploit:exploit-1", EDGE_HAS_EXPLOIT),
            Edge("Exploit:exploit-1", "Sink:sqli", EDGE_TARGETS_SINK),
        ])
        # Find exploits that target 'sqli' sink
        parents = kg.find_parents("Sink:sqli", NODE_EXPLOIT)
        assert len(parents) == 1
        assert parents[0][0].name == "exploit-1"

    def test_transitive_traversal(self, kg):
        kg.add_node_batch([
            Node(NODE_CVE, "CVE-1"),
            Node(NODE_EXPLOIT, "exploit-1"),
            Node(NODE_SINK, "sqli"),
            Node(NODE_FINDING, "finding-1"),
            Node(NODE_SURFACE, "GET:/login"),
        ])
        kg.add_edge_batch([
            Edge("CVE:CVE-1", "Exploit:exploit-1", EDGE_HAS_EXPLOIT),
            Edge("Exploit:exploit-1", "Sink:sqli", EDGE_TARGETS_SINK),
            Edge("Finding:finding-1", "Sink:sqli", EDGE_USES_SINK),
            Edge("Finding:finding-1", "Surface:GET:/login", EDGE_FOUND_ON),
        ])
        # From CVE-1, find all reachable nodes up to depth 3
        related = kg.find_related("CVE:CVE-1", max_depth=3)
        names = {n.name for n, et in related}
        assert "exploit-1" in names
        assert "sqli" in names

    def test_find_path(self, kg):
        kg.add_node_batch([
            Node(NODE_CVE, "CVE-1"),
            Node(NODE_EXPLOIT, "exploit-1"),
            Node(NODE_SINK, "sqli"),
        ])
        kg.add_edge_batch([
            Edge("CVE:CVE-1", "Exploit:exploit-1", EDGE_HAS_EXPLOIT),
            Edge("Exploit:exploit-1", "Sink:sqli", EDGE_TARGETS_SINK),
        ])
        paths = kg.find_path("CVE:CVE-1", "Sink:sqli")
        assert len(paths) >= 1
        assert "CVE-1" in paths[0]
        assert "sqli" in paths[0]

    def test_no_path(self, kg):
        kg.add_node(Node(NODE_TECHNOLOGY, "react"))
        kg.add_node(Node(NODE_TECHNOLOGY, "vue"))
        paths = kg.find_path("Technology:react", "Technology:vue")
        assert len(paths) == 0


class TestPopulation:
    def test_populate_empty(self, kg):
        """No crash when intel/vectors DBs don't exist."""
        count = kg.populate_from_intel_db("/nonexistent/db.sqlite")
        assert count == 0
        count = kg.populate_from_vectors_db("/nonexistent/db.sqlite")
        assert count == 0

    def test_clear(self, kg):
        kg.add_node(Node(NODE_TECHNOLOGY, "test"))
        assert kg.count_nodes() == 1
        kg.clear()
        assert kg.count_nodes() == 0


class TestStats:
    def test_stats(self, kg):
        kg.add_node(Node(NODE_TECHNOLOGY, "a"))
        kg.add_node(Node(NODE_CVE, "CVE-1"))
        kg.add_edge(Edge("CVE:CVE-1", "Technology:a", EDGE_AFFECTS))
        stats = kg.stats()
        assert stats["total_nodes"] == 2
        assert stats["total_edges"] == 1
        assert stats["nodes_by_type"][NODE_TECHNOLOGY] == 1
        assert stats["size_bytes"] > 0
        assert stats["populated"] is False

    def test_size_bytes(self, kg):
        kg.add_node(Node(NODE_TECHNOLOGY, "test"))
        kg.conn.commit()
        assert kg.size_bytes() > 0


class TestHelpers:
    def test_make_technology_node(self):
        from engine.knowledge_graph import make_technology_node
        n = make_technology_node("react", 0.8, ["_reactroot"])
        assert n.node_type == NODE_TECHNOLOGY
        assert n.name == "react"
        assert n.properties["confidence"] == 0.8
        assert "first_seen" in n.properties

    def test_make_finding_node(self):
        from engine.knowledge_graph import make_finding_node
        n = make_finding_node("finding-42", "sqli_error", "high", 0.95)
        assert n.node_type == NODE_FINDING
        assert n.properties["sink"] == "sqli_error"

    def test_make_surface_node(self):
        from engine.knowledge_graph import make_surface_node
        n = make_surface_node("/api/users", "POST", True, role="admin")
        assert n.name == "POST:/api/users"
        assert n.properties["requires_auth"] is True
        assert n.properties["role"] == "admin"
