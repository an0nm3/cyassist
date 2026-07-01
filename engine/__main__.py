"""CyAssist Engine v2 CLI entrypoint: python -m engine sync|extract|query|status"""

import argparse
import sys
import json

from .storage import MetadataStore
from .index_syncer import IndexSyncer
from .extractor import OnDemandExtractor
from .attack_dna import AttackDNAExporter


def do_sync(args, store):
    syncer = IndexSyncer(store=store, verbose=True)
    if args.src == "all":
        counts = syncer.sync_all()
    elif args.src == "hackerone":
        counts = {"hackerone": syncer.sync_hackerone()}
    elif args.src == "immunefi":
        counts = {"immunefi": syncer.sync_immunefi()}
    elif args.src == "medium":
        counts = {"medium": syncer.sync_medium_feeds()}
    store.close()
    print(json.dumps({
        "new_counts": counts,
        "total_indexed": store.count(),
        "storage_mb": round(store.size_mb(), 2),
    }, indent=2))


def do_extract(args, store):
    dna_dir = args.dna_dir
    ex = OnDemandExtractor(store=store, dna_dir=dna_dir, verbose=True)
    if args.report_id:
        vec = ex.extract_by_report_id(args.report_id)
        if vec:
            print(json.dumps(vec, indent=2))
        else:
            print('{"error": "not found or unreachable"}', file=sys.stderr)
            sys.exit(1)
    else:
        vecs = ex.extract_all(limit=args.limit)
        print(json.dumps({"extracted": len(vecs)}, indent=2))


def do_query(args, store):
    results = []
    for meta in store.list_all():
        if args.cwe and args.cwe.lower() not in (meta.cwe or "").lower():
            continue
        if args.severity:
            sv = getattr(meta, "vulnerability_type", "") or ""
            if args.severity.lower() not in sv.lower():
                continue
        results.append(meta)
    if args.json:
        out = []
        for r in results:
            d = {"id": r.id, "url": r.url, "source": r.source, "title": r.title,
                 "cwe": r.cwe, "cve": r.cve, "platform": r.platform,
                 "vulnerability_type": r.vulnerability_type, "timestamp": r.timestamp}
            out.append(d)
        print(json.dumps(out, indent=2))
    else:
        if not results:
            print("No matching entries.")
            return
        print(f"{'ID':>18}  {'Source':>10}  {'Title':<60}")
        print("-" * 92)
        for r in results[:30]:
            print(f"{r.id:>18}  {r.source:>10}  {r.title[:60]:<60}")


def do_status(args, store):
    dna = AttackDNAExporter(output_dir=args.dna_dir).collect_all()
    sources = {}
    for meta in store.list_all():
        sources[meta.source] = sources.get(meta.source, 0) + 1
    print(json.dumps({
        "total_indexed": store.count(),
        "storage_mb": round(store.size_mb(), 3),
        "sources": sources,
        "dna_vectors": len(dna),
    }, indent=2))


def do_catalog(args, store):
    ex = OnDemandExtractor(store=store, dna_dir=args.dna_dir, verbose=True)
    path = ex.build_catalog()
    if path:
        print(json.dumps({"catalog": path}, indent=2))
    else:
        print('{"error": "no vectors to catalog"}', file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(prog="cyassist-engine")
    parser.add_argument("--db-path", default=None, help="Shelve db path")
    parser.add_argument("--dna-dir", default=None, help="DNA output directory")

    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("sync", help="Sync remote indexes")
    p.add_argument("--src", choices=["hackerone", "immunefi", "medium", "all"],
                   default="all", help="Source to sync")

    p = sub.add_parser("extract", help="Extract attack DNA")
    p.add_argument("--report-id", default="", help="Numeric H1 report ID")
    p.add_argument("--limit", type=int, default=20)

    p = sub.add_parser("query", help="Query indexed reports")
    p.add_argument("--cwe", default="", help="Filter by CWE")
    p.add_argument("--severity", default="", choices=["HIGH", "MEDIUM", "LOW", ""])
    p.add_argument("--json", action="store_true")

    sub.add_parser("status", help="Engine stats")
    sub.add_parser("catalog", help="Rebuild DNA catalog")

    args = parser.parse_args()
    store = MetadataStore(db_path=args.db_path)

    dispatch = {
        "sync": do_sync,
        "extract": do_extract,
        "query": do_query,
        "status": do_status,
        "catalog": do_catalog,
    }
    dispatch[args.command](args, store)


if __name__ == "__main__":
    main()
