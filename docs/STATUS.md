# BGM Status (August 2026)

## Working

| Area | Notes |
|------|--------|
| Firmware HR / SpO₂ / temp | MAX30102 path in `Armband_Full.ino` |
| LIS3DH motion + INT1 wake | Hardware wake + RTC EMA state; INT1 uses **detected** I²C address (0x18 or 0x19); latched — clear via `INT1_SRC` |
| 940 nm channel | Multi-sample + EMA; experimental glucose signal |
| Deep sleep + quiet-wake skip | Power path implemented; GPIO wake API (not ext0) |
| MQTT publish | Topic `armband/ppg`, full JSON payload |
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

## Recent firmware fixes (2026-08-06/08)

In `armband-ppg-940nm` `firmware/Armband_Full.ino`:

- **Deep-sleep GPIO wake** – switched from `esp_sleep_enable_ext0_wakeup` to `esp_deep_sleep_enable_gpio_wakeup` (correct API for ESP32-C3 / XIAO — this chip has no ext0/ext1). Wake-cause check updated to `ESP_SLEEP_WAKEUP_GPIO`.
- **MAX30102 FIFO drain** – buffer fill now uses `check()` / `available()` / `getFIFOIR()` / `getFIFORed()` / `nextSample()` so samples actually advance instead of re-reading the same cached value. Finger/beat detection uses a fresh buffer sample.
- **LIS3DH INT1 I²C address** – `setupLIS3DH_INT1()` / `clearLIS3DH_INT1()` previously hardcoded `0x18`. Firmware now stores the address returned by `lis.begin` (0x18 or 0x19) in `lis3dhAddr` and uses it for all INT1 register traffic. Without this, boards with SA0 tied high never got motion-wake config.

These address the issues that were preventing reliable motion wake and correct PPG sample streams.

**Practical note (latched INT1):** INT1 is active-low and latched. Firmware must read `INT1_SRC` to clear it on wake and again before re-entering deep sleep. A stuck latch can immediately re-wake or block sleep.

## Recent AI / calibration fixes (2026-08-06/08)

In `armband-ai`:

- **still_fraction gate order** – `build_calibration_pairs()` previously computed `still_fraction` *after* filtering to `moving==0` when `prefer_still=True`. That made the fraction trivially 1.0 whenever any still sample existed and silently defeated `min_still_fraction`. It is now computed on the **raw, unfiltered window first**, then the prefer-still filter is applied for feature aggregation.

- **quality_score gate order (2026-08-08)** – `score_dataframe()` was previously called *after* the same prefer-still filter. Because the quality heuristic is dominated by motion terms, scoring the already-cleaned subset silently inflated `quality_score` the same way the still_fraction bug did. Quality is now computed from the raw `WindowFeatures` via `score_window()` **before** prefer-still is applied. Prefer-still still controls which rows are averaged into `filt940_mean` etc.; it no longer affects what is scored or gated.

- **Consecutive-clean streak (2026-08-08)** – `WindowFeatures` now includes `max_clean_streak` and `clean_fraction`. A sample is clean when still *and* optically stable (relative deviation from short rolling median + local range). Calibration accepts `min_clean_streak` (config / `--min-clean-streak`; default 0 = off; recommend 10–15). Quality scoring penalizes short streaks. Prefer-still can no longer cherry-pick short clean snippets inside a noisy window when the streak gate is enabled.

- **MLP training consistency (2026-08-08, second fix)** – `scripts/train_mlp_onnx.py` previously called `build_calibration_pairs()` without `min_clean_streak` (so the consecutive-clean gate was silently skipped for the neural path) and re-filtered stillness with an ad-hoc `>=4 still samples` rule that did not match `prefer_still`. The `quality_score` on a training row could therefore describe a different candidate window than the feature vector being trained. Now passes `min_clean_streak` (CLI default 10) and mirrors `prefer_still` exactly; added `--min-clean-streak` / `--no-prefer-still` for parity with `calibrate.py` and `train_multifeature.py`.

- **Drift monitor (2026-08-08)** – `src/armband_ai/drift_monitor.py`. Maintains still-only rolling median of `filt940`; snapshots baseline at successful calibration (`models/drift_baseline.json`); surfaces `drift` / `is_stale` (advisory, default |Δ| ≥ 40). Does not block inference or alter the 17-float feature contract.

- **Insert-time soft validation (2026-08-08)** – `db.insert_reading` now soft-validates BPM (35–220) and temp (30–45 °C): logs a warning and clamps; never rejects the insert (consistent with SpO₂ < 0 handling).

**Practical note (still_fraction + quality):** Passing `min_still ≥ 0.70` and a non-trivial `min_quality` now means the *raw* window was mostly still and scored well, not “looked good after throwing away the moving samples.” Edge motion can still pass the still gate alone — enable `min_clean_streak` for sustained stable periods.

## Experimental / limited

| Area | Notes |
|------|--------|
| Glucose accuracy | Depends on volume of high-quality still Libre pairs; not medical grade |
| Hailo HEF models | Pipeline ready; needs trained + DFC-compiled HEF on device |
| Motion artifact rejection on PPG | Basic magnitude gate only |
| SpO₂ during heavy motion | Often invalid (`-1`) by design |

## Recommended next priorities

From armband-ai hardening list (highest leverage first):

1. ~~Consecutive-clean streak in quality / calibration pairing~~ **done 2026-08-08**
2. ~~Quality score on raw window~~ **done 2026-08-08**
3. ~~MLP path uses same gates as multi-feature / calibrate~~ **done 2026-08-08**
4. ~~Drift monitor (still-only `filt940` median vs last cal)~~ **done 2026-08-08**
5. ~~Insert-time soft validation (BPM/temp)~~ **done 2026-08-08**
6. Tighter optical CV / range / slope thresholds (partially applied in quality.py)
7. More still Libre pairs → retrain multi-feature and optional MLP
8. Compile and deploy a real HEF once pair count is solid

Firmware-side polish:

- Confirm deep-sleep current with a meter
- Tune INT1 / software motion thresholds on-body
- Decide long-term OLED keep vs remove for battery

## Disclaimer

Experimental personal research. **Not a medical device.**
