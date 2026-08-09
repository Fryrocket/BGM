# BGM Status (August 2026)

## Working

| Area | Notes |
|------|--------|
| Firmware HR / SpO₂ / temp | MAX30102 path in `Armband_Full.ino`; gated on `maxOk` |
| LIS3DH motion + INT1 wake | Hardware wake + RTC EMA state; INT1 uses **detected** I²C address (0x18 or 0x19); latched — clear via `INT1_SRC` |
| 940 nm channel | Multi-sample + EMA; experimental glucose signal; **gpio hold** across deep sleep |
| Deep sleep + quiet-wake skip | Power path implemented; GPIO wake API (not ext0); shorter awake if MAX missing |
| MQTT publish | Topic `armband/ppg`, full JSON payload; bpm/temp/spo2 use −1 sentinels |
| Pi MQTT logger + SQLite | Continuous ingest |
| Feature extraction | 17-vector contract frozen; **+ max_clean_streak / clean_fraction** |
| Quality gates | Still fraction (**raw-window**) + quality score (**raw-window**) + **consecutive-clean streak** |
| CPU baseline + multi-feature | Train / run scripts live; `--min-clean-streak` supported |
| MLP → ONNX path | `train_mlp_onnx.py` now passes `min_clean_streak` and mirrors `prefer_still` exactly |
| Streamlit dashboard | Live + calibration tabs |
| Hailo-8 driver path | diagnose / identify scripts; HEF inference priority in v0.4.2 |
| Libre logging | `log_glucose.py` + calibrate flow |
| **Drift monitor** | still-only filt940 median vs last-cal baseline; advisory `is_stale` (2026-08-08) |
| **Insert-time soft validation** | BPM 35–220 / temp 30–45 °C log+clamp on insert (2026-08-08) |
| **iOS companion** | Parser rejects ≤0 vitals; ReadingStore capped (5000) + prune; dual independent charts |

## Recent firmware fixes (2026-08-06/08)

In `armband-ppg-940nm` `firmware/Armband_Full.ino`:

- **Deep-sleep GPIO wake** – `esp_deep_sleep_enable_gpio_wakeup` (ESP32-C3).
- **MAX30102 FIFO drain** – proper `check()` / FIFO advance.
- **LIS3DH INT1 I²C address** – `lis3dhAddr` used everywhere (0x18 or 0x19).

## Firmware polish (2026-08-09 PM) — second-opinion review

Verified against HEAD; Claude’s Drive copy was stale for several items.

**Implemented:**

- **`maxOk` / `lisOk` gates** – PPG path skipped if MAX30102 `begin` fails; awake window capped at 3 s when MAX missing (not an infinite loop — outer FIFO fill already had a 2.5 s timeout).
- **`gpio_hold_en` on 940 nm emitter** – pin held LOW across deep sleep; released on wake.
- **Phantom motion transition suppress** – on GPIO wake, `prevIsMoving = true` + one-shot `suppressTransition` so the first `updateMotion()` does not log a synthetic still↔moving edge.

**Confirmed already fixed at HEAD (do not re-open):**

- LIS3DH address auto-detect
- bpm/temp/spo2 −1 sentinels via `fingerDetected` / `tempValid` / `validSPO2`

## iOS polish (2026-08-09 PM)

- **`Reading.fromFirmwareJSON`** – NSNumber-safe; rejects `<= 0` for bpm/spo2/temp; robust `moving` parse.
- **`ReadingStore`** – hard cap 5000; prune oldest **synced** first; incremental `pendingCount`.
- **`DashboardView`** – separate BPM and 940 nm charts with independent y-domains (no more dual LineMark / shared axis).

## Recent AI / calibration fixes (2026-08-06/08)

(Unchanged — see prior notes for still_fraction / quality / clean streak / drift / soft validation.)

## Experimental / limited

| Area | Notes |
|------|--------|
| Glucose accuracy | Depends on volume of high-quality still Libre pairs; not medical grade |
| Hailo HEF models | Pipeline ready; needs trained + DFC-compiled HEF on device |
| Motion artifact rejection on PPG | Basic magnitude gate only |
| SpO₂ during heavy motion | Often invalid (`-1`) by design |

## Recommended next priorities

1. Confirm deep-sleep current with a meter (after gpio hold)
2. Tune INT1 / software motion thresholds on-body
3. More still Libre pairs → retrain
4. Drive housekeeping (duplicate manuals, versioned filenames)
5. Optional: EMA seed flags instead of magic thresholds

## Disclaimer

Experimental personal research. **Not a medical device.**
