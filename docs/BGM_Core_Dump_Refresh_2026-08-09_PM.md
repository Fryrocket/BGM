# BGM Core Dump — Refresh Addendum (2026-08-09 evening CDT)

**Purpose:** Bring the Core Dump current after afternoon firmware/iOS polish, Drive hygiene, git bundles, and experiment protocol.
**Primary Doc:** https://docs.google.com/document/d/1I5eAHAKOKOWijYORzmjhthp5357BXqfRVNg_ueDer0o/edit
**Authority:** Grok (PM). Claude = editor only, no GitHub.

---

## 1. How to restore (replaces aspirational §10 language)

`00_Project_Backups/bundles/` (and `BGM/bundles/`) holds a dated **git bundle** for each repo, full history, all branches.

```
git clone BGM-2026-08-09.bundle BGM
git clone armband-ppg-940nm-2026-08-09.bundle armband-ppg-940nm
git clone armband-ai-2026-08-09.bundle armband-ai
git clone armband-ios-2026-08-09.bundle armband-ios
```

See `RESTORE.txt` in that folder. **Bundles are the restore path.** This document is the human-readable companion (status, contracts, trees). Sections that say "see the repo" are intentional — the PDF/Doc is not a rebuild artifact.

Nightly automation (install from `BGM/docs/automation/`): mirror clones → `git bundle create` → `git bundle verify` → push to Drive → prune 14d; Drive snapshot excludes `bundles/**` and is not aborted by git failures.

---

## 2. Firmware HEAD (F1–F8 closed)

Implemented 2026-08-09: maxOk/lisOk, gpio hold on 940 nm emitter, phantom GPIO-wake transition suppress, RTC EMA seed flags (`rtcHave940` / `rtcHaveMotion`), static_assert on wake GPIO ≤5.
Already correct before review: lis3dhAddr, −1 sentinels, FIFO timeout pattern.

Do **not** re-open F1–F8.

---

## 3. iOS HEAD

Parser NSNumber-safe + ≤0 → nil; ReadingStore cap 5000 prune synced first; dual independent charts. Fix Pack 2 ACK/idempotency on SyncEngine (repo).

---

## 4. Experiment vs pipeline

Calibration folders and model folders are **empty**. Sheets are headers-only. Quality thresholds are **simulation-derived** until real windows exist.

**S001** (plumbing, no Libre): checklist filed. Capture filt940 range, max_clean_streak on skin, score __/21.
**S002+**: calibration + re-seat / flat-Libre negative controls; tag `Band_Placement_ID` and Notes.

Suggested sheet columns before any data: Session Log `Band_Placement_ID`; Tracker `Ambient_Temp_C`, `Skin_Temp_C`, `filt940_sd` (± optional `Time_Since_Placement_min`).

---

## 5. Drive hygiene (done / open)

**Done:** root manual duplicates trashed; README/rclone/checklist collisions resolved; status snapshot refreshed; RESTORE.txt; S001 checklist Doc.
**Open (Fry UI):** PDF renames in `07_iOS_App` by size; move SOW/Addendum/Core Dump Docs into proper subfolders (native Move, not re-upload).

---

## 6. Repos

| Repo | Role |
|------|------|
| BGM | Umbrella, docs, automation, S001 checklist |
| armband-ppg-940nm | Firmware |
| armband-ai | Pi logger, features, quality, models |
| armband-ios | SwiftUI companion |

GitHub HEAD is truth. Claude has **no** GitHub — keep this Core Dump current after every real change.

---

Experimental research only. **Not a medical device.**
