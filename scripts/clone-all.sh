#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Fryrocket
#
# Clone all BGM component repos into this workspace.
# Run from the BGM repo root.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

FIRMWARE_DIR="firmware"
HOST_DIR="host"
IOS_DIR="ios"
FIRMWARE_URL="https://github.com/Fryrocket/armband-ppg-940nm.git"
HOST_URL="https://github.com/Fryrocket/armband-ai.git"
IOS_URL="https://github.com/Fryrocket/armband-ios.git"

clone_or_update() {
  local dir="$1"
  local url="$2"
  local name="$3"

  if [[ -d "$dir/.git" ]]; then
    echo "==> Updating $name in $dir"
    git -C "$dir" pull --ff-only || git -C "$dir" pull --rebase
  elif [[ -e "$dir" ]]; then
    echo "ERROR: $dir exists but is not a git repo. Move it aside and re-run." >&2
    exit 1
  else
    echo "==> Cloning $name → $dir"
    git clone "$url" "$dir"
  fi
}

clone_or_update "$FIRMWARE_DIR" "$FIRMWARE_URL" "armband-ppg-940nm"
clone_or_update "$HOST_DIR" "$HOST_URL" "armband-ai"
clone_or_update "$IOS_DIR" "$IOS_URL" "armband-ios"

echo
echo "Workspace ready:"
echo "  $ROOT/$FIRMWARE_DIR  (firmware)"
echo "  $ROOT/$HOST_DIR      (Pi host)"
echo "  $ROOT/$IOS_DIR       (iPhone companion)"
echo
echo "Next: docs/SETUP_FULL.md"
