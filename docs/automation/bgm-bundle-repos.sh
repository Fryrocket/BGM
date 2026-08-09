#!/bin/bash
# Mirror the four BGM repos and cut dated bundles, then push to Drive.
# Install: sudo cp docs/automation/bgm-bundle-repos.sh /usr/local/bin/ && sudo chmod +x /usr/local/bin/bgm-bundle-repos.sh
#
# NOTE: deliberately not `set -e` — a git failure must not abort the
# Drive snapshot that runs after this. Each repo fails independently.
set -uo pipefail

MIRROR_ROOT="/var/backups/bgm-mirrors"
BUNDLE_ROOT="/var/backups/bgm-drive/bundles"
LOG="/var/backups/bgm-drive/bgm-drive-backup.log"
STAMP=$(date +%F)
REPOS="BGM armband-ppg-940nm armband-ai armband-ios"

mkdir -p "$MIRROR_ROOT" "$BUNDLE_ROOT"

for r in $REPOS; do
  M="$MIRROR_ROOT/$r.git"

  if [ ! -d "$M" ]; then
    git clone --mirror "https://github.com/Fryrocket/$r.git" "$M" >>"$LOG" 2>&1 \
      || { echo "[$(date -Iseconds)] clone FAILED: $r" >>"$LOG"; continue; }
  else
    git -C "$M" remote update --prune >>"$LOG" 2>&1 \
      || { echo "[$(date -Iseconds)] fetch FAILED: $r" >>"$LOG"; continue; }
  fi

  B="$BUNDLE_ROOT/$r-$STAMP.bundle"
  git -C "$M" bundle create "$B" --all >>"$LOG" 2>&1 \
    || { echo "[$(date -Iseconds)] bundle FAILED: $r" >>"$LOG"; continue; }

  # Prove it is actually restorable, not merely present.
  git bundle verify "$B" >>"$LOG" 2>&1 \
    || echo "[$(date -Iseconds)] VERIFY FAILED: $r" >>"$LOG"
done

# Push up, then prune to 14 days on both sides.
rclone copy "$BUNDLE_ROOT" gdrive:BGM/bundles \
  --log-file="$LOG" --log-level INFO
rclone delete gdrive:BGM/bundles --min-age 14d --log-file="$LOG"
find "$BUNDLE_ROOT" -name "*.bundle" -mtime +14 -delete

echo "[$(date -Iseconds)] Bundle pass complete" >>"$LOG"
# Always exit 0 so systemd ExecStartPre does not abort the Drive snapshot.
exit 0
