#!/usr/bin/env python3
"""Cyassist v2.1 — unified CLI for Indian news, exploit DNA, template sync, Rudra bridge.
v2.1: Added -i/--india flag for instant Indian news reader dispatch.
Storage target: <100MB. SQLite-backed. No exploit code cached."""

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
        "harvest": "harvester",
        "templates": "template_sync",
        "bridge": "rudra_bridge",
        "on-demand": "on_demand",
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
    p = argparse.ArgumentParser(description="Cyassist v2 — intel-driven bug bounty assistant")
    p.add_argument("--status", action="store_true", help="Show intel DB stats")
    p.add_argument("--size", action="store_true", help="Show DB size only")

    # News
    p.add_argument("--news-india", action="store_true", help="Scrape Indian news sources (CERT-In, ET CISO, etc.)")
    p.add_argument("--news-web", action="store_true", help="Scrape web news (THN, BleepingComputer, Reddit, X)")

    # Exploit DNA
    p.add_argument("--harvest", action="store_true", help="Harvest exploit DNA from Exploit-DB/GitHub")
    p.add_argument("--harvest-cve", metavar="CVE-ID", help="Harvest GitHub PoCs for a specific CVE")

    # Template sync
    p.add_argument("--sync-templates", action="store_true", help="Index nuclei + Metasploit templates")
    p.add_argument("--check-templates", action="store_true", help="Check if nuclei-templates/Metasploit exist")

    # Rudra bridge
    p.add_argument("--tech", metavar="TECH", help="Look up CVEs for a technology")
    p.add_argument("--cve", metavar="CVE-ID", help="Show CVE intel + probe config")
    p.add_argument("--auto-scan", metavar="URL", help="Generate Rudra scan config for target")

    # On-demand
    p.add_argument("--fetch-exploit", metavar="URL", help="Fetch exploit code (no cache, read-only)")
    p.add_argument("--fetch-cve", metavar="CVE-ID", help="Show stored exploit URLs for a CVE")
    p.add_argument("--nuclei", metavar="URL", help="Run nuclei templates against target")
    p.add_argument("--nuclei-cve", metavar="CVE-ID", help="Run nuclei for a specific CVE")

    # Watch mode
    p.add_argument("--watch", action="store_true", help="Watch mode — monitors for new intel")
    p.add_argument("--watch-interval", type=int, default=300, help="Watch polling interval (s)")
    p.add_argument("--auto-scan-watch", action="store_true", help="Auto-trigger scans on relevant CVEs")

    # Reader
    p.add_argument("--reader", action="store_true", help="Launch news reader (reader.py)")
    p.add_argument("-i", "--india", action="store_true",
                   help="India preset scope (cert-in, dpdp, aadhaar, indian banks)")
    p.add_argument("--hunt", action="store_true", help="Run hunting pipeline (hunter.py)")
    p.add_argument("--poc", action="store_true", help="Show PoCs from hunter")

    # Pipeline
    p.add_argument("--daily", action="store_true", help="Daily auto-run: scrape + harvest + sync")

    args = p.parse_args()

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
                print(f"\n  {Fmt.bold('Cyassist v2 — Intel DB')}")
                sz = stats["size_mb"]
                print(f"  Size:     {Fmt.cyan(f'{sz:.2f}MB')} "
                      f"{Fmt.dim('(target: <100MB)')}")
                print(f"  CVEs:     {stats['cves']}")
                print(f"  Exploits: {stats['exploits']}  {Fmt.dim('(DNA only, no code)')}")
                print(f"  Templates:{stats['templates']}  {Fmt.dim('(IDs only, no YAML)')}")
                print(f"  Tech map: {stats['tech_cve']}")
                print(f"  News:     {stats['news']}  {Fmt.dim('(metadata only)')}")
                print(f"  Targets:  {stats['targets']}")
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

    # ── Exploit DNA ──
    if args.harvest:
        if args.harvest_cve:
            _dispatch("harvester", ["--cve", args.harvest_cve])
        else:
            _dispatch("harvester")
        return

    # ── Template sync ──
    if args.sync_templates:
        _dispatch("template_sync")
        return
    if args.check_templates:
        _dispatch("template_sync", ["--check"])
        return

    # ── Rudra bridge ──
    if args.tech:
        _dispatch("rudra_bridge", ["--tech", args.tech])
        return
    if args.cve:
        _dispatch("rudra_bridge", ["--cve", args.cve])
        return
    if args.auto_scan:
        _dispatch("rudra_bridge", ["--auto-scan", args.auto_scan])
        return

    # ── On-demand ──
    if args.fetch_exploit:
        _dispatch("on_demand", ["--fetch-exploit", args.fetch_exploit])
        return
    if args.fetch_cve:
        _dispatch("on_demand", ["--fetch-cve", args.fetch_cve])
        return
    if args.nuclei:
        nuc_args = ["--nuclei", args.nuclei]
        if args.nuclei_cve:
            nuc_args += ["--nuclei-cve", args.nuclei_cve]
        _dispatch("on_demand", nuc_args)
        return

    # ── Watch ──
    if args.watch:
        watch_args = ["--watch", "--watch-interval", str(args.watch_interval)]
        if args.auto_scan_watch:
            watch_args.append("--auto-scan")
        _dispatch("on_demand", watch_args)
        return

    # ── Reader (with optional India mode) ──
    if args.india or args.reader:
        reader_args = []
        if args.india:
            reader_args.append("-i")
        if args.reader:
            _dispatch("reader", reader_args if reader_args else None)
        else:
            _dispatch("reader", reader_args)
        return
    if args.hunt or args.poc:
        _dispatch("hunter", [arg for arg in ["--hunt", "--poc"] if getattr(args, arg.strip("-").replace("-", "_"))])
        return

    # ── Daily auto-run ──
    if args.daily:
        print(f"  {Fmt.bold('Cyassist daily auto-run')}")
        print(f"  {Fmt.dim(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))}")
        print()
        _dispatch("scraper_india")
        _dispatch("scraper_web")
        _dispatch("harvester")
        # Template sync is optional (only if templates exist)
        try:
            _dispatch("template_sync")
        except Exception:
            pass
        _dispatch("rudra_bridge", ["--import-targets"])
        try:
            from intel_db import IntelDB
            db = IntelDB()
            stats = db.stats()
            db.close()
            sz = stats["size_mb"]
            cves = stats["cves"]
            exps = stats["exploits"]
            print(f"\n  {Fmt.green('Daily run complete')}  "
                  f"{Fmt.dim(f'{sz:.2f}MB, {cves} CVEs, {exps} exploits')}")
        except ImportError:
            pass
        return

    p.print_help()


if __name__ == "__main__":
    try:
        import datetime
    except ImportError:
        pass
    main()
