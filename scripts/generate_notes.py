#!/usr/bin/env python3
"""Generate standardized BGM notes for Claude (editor) and Gemini (security).

Usage:
  python scripts/generate_notes.py \\
    --title "Subject_ID + homogeneity lock" \\
    --what "armband-ai 0.5.0: homogeneity gate, models restored, --subject-map" \\
    --what "Drive: BGM_Decisions_2026-08-12 uploaded" \\
    --orders "Treat Decisions doc + armband-ai HEAD as source of truth" \\
    --orders "Do not re-open F1-F8 / schema freeze" \\
    --gemini "Export protocol is edit protection only, not DR" \\
    --gemini "Version-history check still open before production rows" \\
    [--out path.md]

Prints the note to stdout and optionally writes a dated file.
Intended for Grok to run after every significant implementer pass.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


def build_note(
    title: str,
    what: list[str],
    orders: list[str],
    gemini: list[str],
    date_str: str | None = None,
) -> str:
    if date_str is None:
        # Prefer Central (project timezone for Fry)
        try:
            now = datetime.now(ZoneInfo("America/Chicago"))
        except Exception:
            now = datetime.now(timezone.utc)
        date_str = now.strftime("%Y-%m-%d")

    lines: list[str] = []
    lines.append(f"# Notes to Claude (editor) & Gemini (security, read-only)")
    lines.append(f"**From:** Grok (implementer)")
    lines.append(f"**Date:** {date_str}")
    lines.append(f"**Re:** {title}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## What landed")
    lines.append("")
    if what:
        for item in what:
            lines.append(f"- {item}")
    else:
        lines.append("- (none listed)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Orders for Claude")
    lines.append("")
    if orders:
        for i, item in enumerate(orders, 1):
            lines.append(f"{i}. {item}")
    else:
        lines.append("1. No new orders this pass.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Note for Gemini")
    lines.append("")
    if gemini:
        for item in gemini:
            lines.append(f"- {item}")
    else:
        lines.append("- No security notes this pass.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        "Standing rule: after every significant implementer pass, Grok produces a short "
        "dated note in this format so both of you have a durable trail without re-reading "
        "the whole chat."
    )
    lines.append("")
    lines.append("— Grok")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate BGM notes for Claude & Gemini"
    )
    parser.add_argument("--title", required=True, help="Short subject line")
    parser.add_argument(
        "--what",
        action="append",
        default=[],
        help="What landed (repeatable)",
    )
    parser.add_argument(
        "--orders",
        action="append",
        default=[],
        help="Orders for Claude (repeatable)",
    )
    parser.add_argument(
        "--gemini",
        action="append",
        default=[],
        help="Notes for Gemini (repeatable)",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Override date YYYY-MM-DD (default: today Central)",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Optional path to write the markdown file",
    )
    args = parser.parse_args()

    note = build_note(
        title=args.title,
        what=args.what,
        orders=args.orders,
        gemini=args.gemini,
        date_str=args.date,
    )

    print(note)

    if args.out:
        path = Path(args.out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(note, encoding="utf-8")
        print(f"\nWrote → {path}", file=__import__("sys").stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
