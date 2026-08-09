#!/usr/bin/env python3
"""
generate_file_indexes.py
------------------------
Walk one or more BGM component repos and rewrite the "## File index"
section in each README.md with real relative links to every tracked file.

Usage:
  # From the BGM umbrella after clone-all.sh:
  python3 scripts/generate_file_indexes.py

  # Or point at specific repos:
  python3 scripts/generate_file_indexes.py ../armband-ppg-940nm ../armband-ai ../armband-ios

  # Dry-run (print what would be written):
  python3 scripts/generate_file_indexes.py --dry-run

The script only touches the block between:
  ## File index
  ...
  (next ## heading or EOF)

Everything else in the README is left alone.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

# ---------------------------------------------------------------------------
# Configuration per repo
# ---------------------------------------------------------------------------

# Optional short descriptions for important files (shown after the link).
# Anything not listed here just gets the bare link.
DESCRIPTIONS = {
    # armband-ppg-940nm
    "firmware/Armband_Full.ino": "**main firmware** (INT1 wake, 940 nm EMA, MQTT, deep sleep)",
    "firmware/MAX30102_Full_Monitor.ino": "HR/SpO₂/temp + OLED bench sketch",
    "firmware/MAX30102_HeartRate_Temp_OLED.ino": "earlier HR/temp sketch",
    "PINOUT.md": "printable pinout + wire colour card",
    "SETUP.md": "hardware, libraries, config, first run",
    "NOTES.md": "development log and tuning notes",

    # armband-ai
    "src/armband_ai/calibration.py": "fingerstick/Libre pairing, build_calibration_pairs, fit_multifeature",
    "src/armband_ai/config.py": "YAML config loading and defaults",
    "src/armband_ai/db.py": "SQLite writes, insert-time soft validation",
    "src/armband_ai/drift_monitor.py": "still-only rolling median of filt940 vs baseline",
    "src/armband_ai/features.py": "17-float feature vector, clean streak",
    "src/armband_ai/hailo.py": "Hailo HEF inference path",
    "src/armband_ai/inference_service.py": "CPU/MLP/ONNX/Hailo priority",
    "src/armband_ai/logger.py": "MQTT logger, iOS batch receiver + ACK",
    "src/armband_ai/quality.py": "raw-window quality gates",
    "src/armband_ai/queries.py": "read helpers, init_db",
    "dashboard/app.py": "Streamlit live dashboard",

    # armband-ios
    "Sources/App/ArmbandIOSApp.swift": "app entry, dependency wiring, scene-phase flush",
    "Sources/Models/Reading.swift": "data model + firmware JSON parser",
    "Sources/Store/ReadingStore.swift": "offline store, debounced saves, pending queue",
    "Sources/Store/SyncEngine.swift": "batch dump, ACK handling, cancellation",
    "Sources/Store/DeviceIdentity.swift": "stable per-install device id",
    "Sources/Networking/MQTTClient.swift": "CocoaMQTT wrapper, delegate proxy",
    "Sources/Views/ContentView.swift": "tab shell + settings",
    "Sources/Views/DashboardView.swift": "metric cards + Swift Charts",
    "docs/SETUP_CHECKLIST.md": "start here",
    "docs/PROTOCOL.md": "firmware JSON payload",
    "docs/SYNC_SPEC.md": "batch + ACK contract",

    # BGM umbrella
    "docs/ARCHITECTURE.md": "system architecture, feature vector + MQTT contracts",
    "docs/COMPONENTS.md": "hardware bill of materials",
    "docs/MANUAL.md": "user manual",
    "docs/PINOUT.md": "wiring and pin assignments",
    "docs/SETUP_FULL.md": "end-to-end setup path",
    "docs/STATUS.md": "current project status",
}

# Grouping rules: (heading, list of path prefixes or exact names)
# Order matters — first match wins.
GROUP_RULES = [
    ("Firmware", ["firmware/"]),
    ("Sources", ["Sources/"]),
    ("Package — `src/armband_ai/`", ["src/armband_ai/"]),
    ("Dashboard", ["dashboard/"]),
    ("Docs", ["docs/", "PINOUT.md", "SETUP.md", "NOTES.md", "HARDWARE.md"]),
    ("Scripts", ["scripts/"]),
    ("Systemd units", ["systemd/"]),
    ("Build", ["platformio.ini"]),
    ("Config", ["config.example.yaml", "requirements.txt", "LICENSE", ".gitignore"]),
    ("Root", ["LICENSE", ".gitignore"]),
]

SKIP_NAMES = {".git", ".DS_Store", "__pycache__", ".venv", "node_modules", ".pytest_cache"}


def list_tracked_files(repo: Path) -> List[str]:
    """Return sorted relative paths of all files under repo (excluding skip list)."""
    files = []
    for root, dirs, names in os.walk(repo):
        # prune
        dirs[:] = [d for d in dirs if d not in SKIP_NAMES and not d.startswith(".")]
        for name in names:
            if name in SKIP_NAMES or name.startswith("."):
                if name not in {".gitignore"}:  # keep .gitignore
                    continue
            rel = os.path.relpath(os.path.join(root, name), repo)
            if rel == "README.md":
                continue
            files.append(rel.replace(os.sep, "/"))
    return sorted(files)


def group_files(files: List[str]) -> List[Tuple[str, List[str]]]:
    """Assign files to groups according to GROUP_RULES. Unmatched go to 'Other'."""
    groups: dict[str, List[str]] = {}
    used = set()

    for heading, prefixes in GROUP_RULES:
        matched = []
        for f in files:
            if f in used:
                continue
            for p in prefixes:
                if f == p or f.startswith(p):
                    matched.append(f)
                    used.add(f)
                    break
        if matched:
            groups.setdefault(heading, []).extend(matched)

    remaining = [f for f in files if f not in used]
    if remaining:
        groups["Other"] = remaining

    # Preserve a sensible order
    order = [h for h, _ in GROUP_RULES] + ["Other"]
    result = []
    for h in order:
        if h in groups:
            result.append((h, sorted(groups[h])))
    return result


def render_index(groups: List[Tuple[str, List[str]]]) -> str:
    lines = ["## File index", ""]
    for heading, files in groups:
        lines.append(f"**{heading}**")
        for f in files:
            desc = DESCRIPTIONS.get(f, "")
            if desc:
                lines.append(f"- [{f}]({f}) — {desc}")
            else:
                lines.append(f"- [{f}]({f})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def replace_file_index(readme_text: str, new_block: str) -> str:
    """
    Replace existing ## File index section, or append one before the final
    License section if none exists.
    """
    # Match from ## File index up to (but not including) the next ## heading
    pattern = re.compile(
        r"(^## File index\s*\n)(.*?)(?=^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    if pattern.search(readme_text):
        return pattern.sub(new_block + "\n", readme_text, count=1)

    # No existing section — insert before the last ## License / ## License /disclaimer
    license_pat = re.compile(r"(^## License.*)", re.MULTILINE | re.DOTALL)
    m = license_pat.search(readme_text)
    if m:
        return readme_text[: m.start()] + new_block + "\n" + readme_text[m.start() :]

    # Fallback: append at end
    return readme_text.rstrip() + "\n\n" + new_block


def process_repo(repo: Path, dry_run: bool = False) -> bool:
    readme = repo / "README.md"
    if not readme.is_file():
        print(f"  skip {repo.name}: no README.md")
        return False

    files = list_tracked_files(repo)
    if not files:
        print(f"  skip {repo.name}: no files found")
        return False

    groups = group_files(files)
    new_block = render_index(groups)

    original = readme.read_text(encoding="utf-8")
    updated = replace_file_index(original, new_block)

    if updated == original:
        print(f"  {repo.name}: already up to date")
        return False

    if dry_run:
        print(f"  {repo.name}: would update ({len(files)} files indexed)")
        print("--- preview ---")
        print(new_block)
        print("--- end ---")
        return True

    readme.write_text(updated, encoding="utf-8")
    print(f"  {repo.name}: updated ({len(files)} files indexed)")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate/update File index sections in BGM READMEs")
    parser.add_argument(
        "repos",
        nargs="*",
        help="Paths to repos (default: look for sibling component repos + self)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print what would change")
    args = parser.parse_args()

    if args.repos:
        targets = [Path(p).resolve() for p in args.repos]
    else:
        # Default: current dir (BGM) + common sibling locations after clone-all
        here = Path.cwd()
        candidates = [
            here,
            here / "firmware",          # after clone-all layout
            here / "host",
            here.parent / "armband-ppg-940nm",
            here.parent / "armband-ai",
            here.parent / "armband-ios",
            here / "armband-ppg-940nm",
            here / "armband-ai",
            here / "armband-ios",
        ]
        targets = []
        seen = set()
        for c in candidates:
            c = c.resolve()
            if c.is_dir() and (c / "README.md").is_file() and c not in seen:
                targets.append(c)
                seen.add(c)

    if not targets:
        print("No repositories found. Pass paths explicitly.")
        return 1

    print(f"Generating File indexes ({'dry-run' if args.dry_run else 'write'})…")
    changed = 0
    for repo in targets:
        print(f"→ {repo}")
        if process_repo(repo, dry_run=args.dry_run):
            changed += 1

    print(f"Done. {changed} README(s) {'would be' if args.dry_run else ''} updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
