#!/bin/bash
# BGM Google Drive dated snapshot (local offline copy).
# Install: sudo cp docs/automation/bgm-drive-snapshot.sh /usr/local/bin/ && sudo chmod +x ...
set -euo pipefail

REMOTE="gdrive:BGM"
LOCAL_ROOT="/var/backups/bgm-drive"
STAMP=$(date +%Y-%m-%d_%H%M)
DEST="${LOCAL_ROOT}/${STAMP}_snapshot"
LOG="${LOCAL_ROOT}/bgm-drive-backup.log"

mkdir -p "$DEST"

echo "[$(date -Iseconds)] Starting BGM Drive snapshot → $DEST" | tee -a "$LOG"

# Exclude bundles/** — those are pushed up by bgm-bundle-repos.sh and must not
# be re-downloaded into every retained snapshot (wastes ~75MB×14).
rclone copy "$REMOTE" "$DEST" \
  --exclude "bundles/**" \
  --transfers=4 \
  --checkers=8 \
  --drive-chunk-size 64M \
  --log-file="$LOG" \
  --log-level INFO \
  --stats=30s

find "$LOCAL_ROOT" -maxdepth 1 -type d -name "*_snapshot" | sort | head -n -14 | xargs -r rm -rf

echo "[$(date -Iseconds)] Snapshot complete: $DEST" | tee -a "$LOG"
