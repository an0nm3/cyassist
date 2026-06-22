#!/usr/bin/env python3
"""Cyassist notifier — Telegram + Discord alerts for critical hunting intel."""

import json
import os
import sys
from pathlib import Path
from typing import Optional

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

HERE = Path(__file__).parent
CONFIG_FILE = HERE / "config.yaml"

USER_AGENT = "cyassist-notifier/1.0"


class Fmt:
    @classmethod
    def red(cls, s): return f"\033[31m{s}\033[0m"
    @classmethod
    def green(cls, s): return f"\033[32m{s}\033[0m"
    @classmethod
    def yellow(cls, s): return f"\033[33m{s}\033[0m"
    @classmethod
    def bold(cls, s): return f"\033[1m{s}\033[0m"
    @classmethod
    def dim(cls, s): return f"\033[2m{s}\033[0m"


def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            import yaml
            with open(CONFIG_FILE) as f:
                return yaml.safe_load(f) or {}
        except ImportError:
            pass
        try:
            return json.loads(CONFIG_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_config(cfg: dict):
    cfg.setdefault("notifications", {})
    try:
        import yaml
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(cfg, f, default_flow_style=False, sort_keys=False)
    except ImportError:
        CONFIG_FILE.write_text(json.dumps(cfg, indent=2))


def setup_telegram(token: str = "", chat_id: str = ""):
    """Configure Telegram bot credentials."""
    cfg = load_config()
    n = cfg.setdefault("notifications", {})
    t = n.setdefault("telegram", {})
    if token:
        t["bot_token"] = token
    if chat_id:
        t["chat_id"] = chat_id
    save_config(cfg)
    print(f"  {Fmt.green('Telegram configured')}")


def setup_discord(webhook_url: str = ""):
    """Configure Discord webhook URL."""
    cfg = load_config()
    n = cfg.setdefault("notifications", {})
    if webhook_url:
        n["discord_webhook"] = webhook_url
    save_config(cfg)
    print(f"  {Fmt.green('Discord configured')}")


def send_telegram(message: str, token: str = "", chat_id: str = "") -> bool:
    """Send a message via Telegram bot."""
    if not HAS_REQUESTS:
        print(f"  {Fmt.red('requests library required for Telegram')}", file=sys.stderr)
        return False
    cfg = load_config()
    t_cfg = cfg.get("notifications", {}).get("telegram", {})
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "") or t_cfg.get("bot_token", "")
    chat = os.environ.get("TELEGRAM_CHAT_ID", "") or t_cfg.get("chat_id", "")
    if token:
        bot_token = token
    if chat_id:
        chat = chat_id
    if not bot_token or not chat:
        print(f"  {Fmt.yellow('Telegram not configured. Use --setup-telegram or set TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID')}", file=sys.stderr)
        return False
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        resp = requests.post(url, json={
            "chat_id": chat,
            "text": message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True,
        }, timeout=15)
        if resp.status_code != 200:
            print(f"  {Fmt.red(f'Telegram API error: {resp.status_code} {resp.text[:200]}')}", file=sys.stderr)
            return False
        return True
    except Exception as e:
        print(f"  {Fmt.red(f'Telegram send failed: {e}')}", file=sys.stderr)
        return False


def send_discord(message: str, webhook_url: str = "") -> bool:
    """Send a message via Discord webhook."""
    if not HAS_REQUESTS:
        print(f"  {Fmt.red('requests library required for Discord')}", file=sys.stderr)
        return False
    cfg = load_config()
    wh = webhook_url or os.environ.get("DISCORD_WEBHOOK", "") or cfg.get("notifications", {}).get("discord_webhook", "")
    if not wh:
        print(f"  {Fmt.yellow('Discord not configured. Use --setup-discord or set DISCORD_WEBHOOK')}", file=sys.stderr)
        return False
    try:
        resp = requests.post(wh, json={
            "content": message,
            "username": "Cyassist Hunter",
        }, timeout=15)
        if resp.status_code not in (200, 204):
            print(f"  {Fmt.red(f'Discord webhook error: {resp.status_code}')}", file=sys.stderr)
            return False
        return True
    except Exception as e:
        print(f"  {Fmt.red(f'Discord send failed: {e}')}", file=sys.stderr)
        return False


def alert_critical(enriched: dict, target_map: dict, brief_file: str = ""):
    """Send alerts for critical/high CVEs matched to targets."""
    critical = {c: i for c, i in enriched.items()
                if i.get("priority_label") in ("CRITICAL", "HIGH") and i.get("priority_score", 0) >= 50}
    if not critical:
        return

    lines = ["**Cyassist Alert — High Priority CVEs**", ""]
    for cve_id, info in sorted(critical.items(),
                                key=lambda x: x[1].get("priority_score", 0), reverse=True)[:10]:
        pri = info.get("priority_label", "INFO")
        cvss = info.get("cvss", "N/A")
        epss = info.get("epss", 0)
        kev = " [KEV]" if info.get("in_kev") else ""
        poc = " [PoC]" if info.get("has_poc") else ""
        desc = info.get("description", "")[:150]
        lines.append(f"*{pri}* `{cve_id}` CVSS:{cvss} EPSS:{epss:.4f}{kev}{poc}")
        if desc:
            lines.append(f"  _{desc}_")
    if brief_file:
        lines.append(f"")
        lines.append(f"Brief: `{brief_file}`")

    msg = "\n".join(lines)
    send_telegram(msg)
    send_discord(msg)


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Cyassist notifier")
    p.add_argument("--setup-telegram", nargs=2, metavar=("TOKEN", "CHAT_ID"),
                   help="Configure Telegram bot token and chat ID")
    p.add_argument("--setup-discord", metavar="WEBHOOK_URL",
                   help="Configure Discord webhook URL")
    p.add_argument("--test", action="store_true", help="Send test message")
    args = p.parse_args()

    if args.setup_telegram:
        setup_telegram(*args.setup_telegram)
    elif args.setup_discord:
        setup_discord(args.setup_discord)
    elif args.test:
        msg = "Cyassist test notification — hunter engine is running."
        tg = send_telegram(msg)
        dc = send_discord(msg)
        print(f"  Telegram: {'OK' if tg else 'SKIP'}")
        print(f"  Discord:  {'OK' if dc else 'SKIP'}")
    else:
        p.print_help()
