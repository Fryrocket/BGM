# BGM Google Drive Backup with rclone (Corrected + bundles)

Automatic offline copy of the BGM Google Drive folder **and** dated `git bundle`s of all four repos.

## Critical corrections (2026-08-09)

1. **Service user must match the user that ran `rclone config`.** Token lives in `~/.config/rclone/rclone.conf`.
2. **Log under** `/var/backups/bgm-drive/bgm-drive-backup.log` (not `/var/log`).
3. **Cleanup keeps last 14 snapshots.**
4. **Git bundles** are cut from `git clone --mirror` caches, verified, pushed to `gdrive:BGM/bundles/`, pruned at 14 days.
5. **Snapshot pull excludes `bundles/**`** so the Pi does not re-download what it just uploaded into every snapshot dir.
6. **Bundle step fails soft** — never aborts the Drive snapshot if GitHub is briefly unreachable.

## One-time setup on the Pi

```bash
sudo apt update && sudo apt install -y rclone git
rclone config   # remote name: gdrive — same user as systemd User=
sudo mkdir -p /var/backups/bgm-drive /var/backups/bgm-mirrors
sudo chown $USER:$USER /var/backups/bgm-drive /var/backups/bgm-mirrors
```

Copy scripts from this repo:

```bash
sudo cp docs/automation/bgm-bundle-repos.sh /usr/local/bin/
sudo cp docs/automation/bgm-drive-snapshot.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/bgm-bundle-repos.sh /usr/local/bin/bgm-drive-snapshot.sh
# edit User=/Group= in the service unit:
sudo cp docs/automation/bgm-drive-backup.service /etc/systemd/system/
sudo cp docs/automation/bgm-drive-backup.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now bgm-drive-backup.timer
```

Test once:

```bash
/usr/local/bin/bgm-bundle-repos.sh
/usr/local/bin/bgm-drive-snapshot.sh
rclone ls gdrive:BGM/bundles --max-depth 1
```

## What this protects

- Calibration data & sheets
- Hardware photos
- Firmware backups
- Complete Backup PDFs / Core Dump companions
- Architecture / status notes
- Future model files and logs
- **`bundles/`** — full git history for BGM, armband-ppg-940nm, armband-ai, armband-ios (offline even if GitHub is down)

Restore a repo: `git clone BGM-YYYY-MM-DD.bundle BGM` (see `RESTORE.txt` in Drive `BGM/bundles/`).

Together with the four GitHub repositories (when reachable) you have both live versioned code and automatic offline copies of Drive **and** git history.

---

Generated / corrected 2026-08-09 for the BGM project. Bundle wiring per editor proposal + Grok implement.
