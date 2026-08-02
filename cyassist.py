#!/usr/bin/env python3
"""Cyassist — unified CLI for cybersecurity news.

Scrapes Indian + global security news sources into a local archive and
browses them from the terminal. SQLite-backed news index. No blobs."""

VERSION = "3.0"

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).parent


class Fmt:
    _no_color = not sys.stdout.isatty()
    @classmethod
    def _w(cls, c, s, r="0"):
        if cls._no_color or not s: return s
        return f"\033[{c}m{s}\033[{r}m"
    @classmethod
    def green(cls, s): return cls._w("32", s)
    @classmethod
    def red(cls, s): return cls._w("31", s)
    @classmethod
    def yellow(cls, s): return cls._w("33", s)
    @classmethod
    def bold(cls, s): return cls._w("1", s)
    @classmethod
    def dim(cls, s): return cls._w("2", s)
    @classmethod
    def cyan(cls, s): return cls._w("36", s)


def _dispatch(module: str, args: list[str] = None):
    """Run a sub-module with given args."""
    module_map = {
        "scrape-india": "scraper_india",
        "scrape-web": "scraper_web",
        "reader": "reader",
        "db": "intel_db",
    }
    mod_name = module_map.get(module, module)
    mod_path = HERE / f"{mod_name}.py"
    if not mod_path.exists():
        print(f"  {Fmt.red(f'Module not found: {mod_path}')}")
        return
    import runpy
    old_argv = list(sys.argv)
    if args:
        sys.argv = [str(mod_path)] + args
    else:
        sys.argv = [str(mod_path)]
    try:
        runpy.run_path(str(mod_path), run_name="__main__")
    finally:
        sys.argv = old_argv


def main():
    p = argparse.ArgumentParser(description="Cyassist — cybersecurity news reader")
    p.add_argument("-v", "--version", action="store_true", help="Show version and exit")
    p.add_argument("--size", action="store_true", help="Show DB size only (machine-readable)")
    p.add_argument("--status", action="store_true", help="Show full DB status")

    # News
    p.add_argument("--news-india", action="store_true", help="Scrape Indian news sources (CERT-In, ET CISO, etc.)")
    p.add_argument("--news-web", action="store_true", help="Scrape web news (THN, BleepingComputer, Reddit, X)")

    # Reader
    p.add_argument("--reader", action="store_true", help="Launch news reader (reader.py)")
    p.add_argument("-i", "--india", action="store_true",
                   help="India preset scope (cert-in, dpdp, aadhaar, indian banks)")
    p.add_argument("-t", "--today", action="store_true", help="Today's headlines (reader)")
    p.add_argument("-T", "--headlines", action="store_true", help="Quick headlines (reader)")
    p.add_argument("-H", "--summary", action="store_true", help="News summary (reader)")
    p.add_argument("-c", "--category", nargs='?', const='__help__', default="",
                   choices=["news", "", "__help__"],
                   help="Category (news)")
    p.add_argument("-q", "--query", nargs='?', const='__help__', default="",
                   help="Search keyword")
    p.add_argument("-s", "--source", nargs='?', const='__help__', default="",
                   help="Filter by source name")
    p.add_argument("-n", "--count", action="store_true", help="Count only")

    # Pipeline
    p.add_argument("--daily", action="store_true", help="Daily auto-run: scrape India + web news")

    args = p.parse_args()

    # ── Version ──
    if args.version:
        print(f"Cyassist v{VERSION}")
        print("Cybersecurity news reader")
        return

    # ── Status / Size ──
    if args.size or args.status:
        try:
            from intel_db import IntelDB
            db = IntelDB()
            stats = db.stats()
            db.close()
            if args.size:
                print(f"{stats['size_mb']:.3f}")
            else:
                print(f"\n  {Fmt.bold('Cyassist — News DB')}")
                sz = stats["size_mb"]
                print(f"  Size:     {Fmt.cyan(f'{sz:.2f}MB')}")
                print(f"  News:     {stats['news']}  {Fmt.dim('(metadata only)')}")
        except ImportError:
            print(f"  {Fmt.red('intel_db.py not available')}")
        return

    # ── News ──
    if args.news_india:
        _dispatch("scraper_india")
        return
    if args.news_web:
        _dispatch("scraper_web")
        return

    # ── Reader (with optional India mode + short flags) ──
    reader_flags = [args.reader, args.today, args.headlines, args.summary,
                    args.category, args.query or args.source, args.count]
    if args.india or args.reader or any(reader_flags):
        reader_args = []
        if args.india:
            reader_args.append("-i")
        if args.today:
            reader_args.append("--today")
        if args.headlines:
            reader_args.append("--headlines")
        if args.summary:
            reader_args.append("--summary")
        if args.category and args.category != "__help__":
            reader_args += ["--category", args.category]
        if args.query and args.query != "__help__":
            reader_args += ["--query", args.query]
        if args.source and args.source != "__help__":
            reader_args += ["--source", args.source]
        if args.count:
            reader_args.append("--count")
        _dispatch("reader", reader_args if reader_args else None)
        return

    # ── Daily auto-run ──
    if args.daily:
        print(f"  {Fmt.bold('Cyassist daily news run')}")
        try:
            import datetime
            print(f"  {Fmt.dim(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))}")
        except ImportError:
            pass
        print()
        _dispatch("scraper_india")
        _dispatch("scraper_web")
        try:
            from intel_db import IntelDB
            db = IntelDB()
            stats = db.stats()
            db.close()
            print(f"\n  {Fmt.green('Daily run complete')}  "
                  f"{Fmt.dim(str(stats['size_mb']) + 'MB, ' + str(stats['news']) + ' articles')}")
        except ImportError:
            pass
        return

    p.print_help()


if __name__ == "__main__":
    main()
