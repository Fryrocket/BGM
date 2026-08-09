# BGM Status (2026-08-09 evening CDT)

## Working

| Area | Notes |
|------|--------|
| Firmware HR / SpO₂ / temp | MAX30102; gated on `maxOk` |
| LIS3DH motion + INT1 wake | `lis3dhAddr` 0x18/0x19; latched INT1 clear; C3 GPIO wake API |
| 940 nm channel | Multi-sample + EMA; **gpio hold** across deep sleep; **RTC EMA seed flags** (no magic thresholds) |
| Deep sleep + quiet-wake skip | GPIO wake; shorter awake if MAX missing; **static_assert** wake pin ≤5 |
| MQTT publish | `armband/ppg`; bpm/spo2/temp −1 sentinels |
| Pi MQTT logger + SQLite | Continuous ingest |
| Feature extraction | 17-vector + clean streak |
| Quality gates | Still fraction + quality + consecutive-clean streak (thresholds from simulation — provisional until real data) |
| CPU / MLP→ONNX / Hailo path | Scripts live; HEF needs trained model on device |
| Streamlit dashboard | Live + calibration |
| Drift monitor | still-only filt940 median; advisory `is_stale` |
| Insert soft validation | BPM/temp clamp on insert |
| **iOS companion** | Parser ≤0→nil; store cap 5000 + prune; dual charts; Fix Pack 2 ACK path |

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

## Offline restore

`BGM/bundles/` on Drive holds dated `git bundle` for all four repos + `RESTORE.txt`.
Automation scripts: `BGM/docs/automation/` (bundle + snapshot + systemd). Install on Pi.

## Experiment status

| Folder / sheet | State |
|----------------|--------|
| Calibration / models / logs / photos | **Empty** — pipeline ahead of data |
| Calibration Tracker / Session Log | Headers only (+ example row) |
| **Next** | Sheet columns (`Band_Placement_ID`, temps, `filt940_sd`) → **S001 plumbing** → S002 calibration with re-seat controls |

S001 checklist: `docs/S001_Plumbing_Verification_Checklist.md` + Drive Doc under `07_iOS_App/Requirements_and_Notes/`.

## Recommended next (human / wrist)

1. Add sheet columns before any data rows
2. Run S001 (21-item plumbing checklist)
3. Meter deep-sleep µA (checklist in Drive)
4. S002+ with re-seat / flat-Libre negative controls
5. Pi: install nightly bundle scripts from `docs/automation/`

## Disclaimer

Experimental personal research. **Not a medical device.**
