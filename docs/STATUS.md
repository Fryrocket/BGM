# BGM Status (2026-08-12)

## Working

| Area | Notes |
|------|--------|
| Firmware HR / SpO₂ / temp | MAX30102; gated on `maxOk` |
| LIS3DH motion + INT1 wake | `lis3dhAddr` 0x18/0x19; latched INT1 clear; C3 GPIO wake API |
| 940 nm channel | Multi-sample + EMA; **gpio hold** across deep sleep; **RTC EMA seed flags** (no magic thresholds) |
| Deep sleep + quiet-wake skip | GPIO wake; shorter awake if MAX missing; **static_assert** wake pin ≤5 |
| MQTT publish | `armband/ppg`; bpm/spo2/temp −1 sentinels |
| Pi MQTT logger + SQLite | Continuous ingest; per-reading `session_id` |
| Feature extraction | Two contracts: **17-vector** (Hailo/MLP, frozen in `features.py`) and **10-feature OLS subset** (`DEFAULT_FEATURE_KEYS` in `models.py`). Clean streak computed on both paths. |
| Quality gates | Still fraction + quality + consecutive-clean streak — **code implemented, never exercised on real pairs** |
| CPU / MLP→ONNX / Hailo path | Scripts live; HEF needs trained model on device. Multi-feature OLS has structural n ≤ p bar (p=10). |
| Streamlit dashboard | Live + calibration |
| Drift monitor | still-only filt940 median; advisory `is_stale` |
| Insert soft validation | BPM/temp clamp on insert |
| **iOS companion** | Parser ≤0→nil; store cap 5000 + prune; dual charts; Fix Pack 2 ACK path; cancel dump |
| **Calibration / Subject_ID** | Homogeneity + per-subject fits + `MIN_PAIRS_PER_SUBJECT=20` + **structural n ≤ p bar** (p=10 for multi-feature OLS). Code paths implemented; **zero real pairs exist** so nothing has been fit yet. `--subject-map` CLI (armband-ai **0.5.0**) |

## Firmware disposition (2026-08-09) — F1–F8 closed

| ID | Item | Status |
|----|------|--------|
| F1 | Infinite MAX loop | Closed — maxOk + 2.5s FIFO + 3s awake cap |
| F2 | LIS3DH hardcode 0x18 | Closed before review |
| F3/F4 | −1 sentinels / junk wake | Closed before review |
| F5 | Phantom transition | Closed — suppressTransition |
| F6 | gpio hold emitter | Closed |
| F7 | EMA magic thresholds | Closed — rtcHave940 / rtcHaveMotion |
| F8 | Wake pin assert | Closed — static_assert |

## Locked decisions (2026-08-11 / 12)

See Drive doc **BGM_Decisions_2026-08-12** (also in BGM folder).

1. **Re-seat = new session** — mid-session re-seat closes the current session and opens a new one with a new Band_Placement_ID.
2. **Homogeneity** — >1 distinct session_id in a pairing window → `dropped_mixed_session`.
3. **Per-subject fits only** — never pool; skip+log `subject_id=None`; refuse under 20 pairs.
4. **Schema freeze** — live Tracker / Session Log IDs only; Fry adds columns by hand if needed later.
5. **Armband_Temp** = MAX30102 die temperature (documented).
6. **Export protocol** — Fry exports both sheets to dated CSV in `02_Calibration_Data` immediately after new rows (edit protection, not DR).

Live sheet IDs:
- Tracker: `17uJJ6bp2dJ9GLERNZFdbtL8_NxvoEfWclgX8TFe5n-w`
- Session Log: `1Jh0geyD5ETSlHHeoTT5A8eONzx44hiOT77aTF9q2zBc`

## Offline restore

`BGM/bundles/` on Drive holds dated `git bundle` for all four repos + `RESTORE.txt`.
Automation scripts: `BGM/docs/automation/` (bundle + snapshot + systemd). Install on Pi.

## Experiment status

| Folder / sheet | State |
|----------------|--------|
| Calibration / models / logs / photos | **Empty** — pipeline ahead of data |
| Calibration Tracker / Session Log | Headers only (+ example row); schema frozen |
| **Next** | **S001 plumbing (Run Sheet ready)** → S002 calibration with re-seat controls |

S001 Run Sheet (one page, pre-filled stub): `docs/S001_Run_Sheet.md`  
(Old checklist redirects to it.)

## Recommended next (human / wrist)

1. Run S001 (Run Sheet) — start export habit on Session Log row
2. Meter deep-sleep µA (checklist in Drive)
3. S002+ with re-seat / flat-Libre negative controls
4. Pi: install nightly bundle scripts from `docs/automation/`
5. Confirm Drive version-history / trash-recovery before first production rows

## Disclaimer

Experimental personal research. **Not a medical device**.
