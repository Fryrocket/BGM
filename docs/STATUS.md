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
| Feature extraction | 17-vector contract frozen |
| Quality gates | Still fraction (**raw-window**) + heuristic score; tighter optical gates recommended |
| CPU baseline + multi-feature | Train / run scripts live |
| Streamlit dashboard | Live + calibration tabs |
| Hailo-8 driver path | diagnose / identify scripts; HEF inference priority in v0.4.2 |
| Libre logging | `log_glucose.py` + calibrate flow |

## Recent firmware fixes (2026-08-06/08)

In `armband-ppg-940nm` `firmware/Armband_Full.ino`:

- **Deep-sleep GPIO wake** – switched from `esp_sleep_enable_ext0_wakeup` to `esp_deep_sleep_enable_gpio_wakeup` (correct API for ESP32-C3 / XIAO — this chip has no ext0/ext1). Wake-cause check updated to `ESP_SLEEP_WAKEUP_GPIO`.
- **MAX30102 FIFO drain** – buffer fill now uses `check()` / `available()` / `getFIFOIR()` / `getFIFORed()` / `nextSample()` so samples actually advance instead of re-reading the same cached value. Finger/beat detection uses a fresh buffer sample.
- **LIS3DH INT1 I²C address** – `setupLIS3DH_INT1()` / `clearLIS3DH_INT1()` previously hardcoded `0x18`. Firmware now stores the address returned by `lis.begin` (0x18 or 0x19) in `lis3dhAddr` and uses it for all INT1 register traffic. Without this, boards with SA0 tied high never got motion-wake config.

These address the issues that were preventing reliable motion wake and correct PPG sample streams.

**Practical note (latched INT1):** INT1 is active-low and latched. Firmware must read `INT1_SRC` to clear it on wake and again before re-entering deep sleep. A stuck latch can immediately re-wake or block sleep.

## Recent AI / calibration fixes (2026-08-06/07)

In `armband-ai` `src/armband_ai/calibration.py`:

- **still_fraction gate order** – `build_calibration_pairs()` previously computed `still_fraction` *after* filtering to `moving==0` when `prefer_still=True`. That made the fraction trivially 1.0 whenever any still sample existed and silently defeated `min_still_fraction`. It is now computed on the **raw, unfiltered window first**, then the prefer-still filter is applied for feature aggregation. Confirmed with adversarial synthetic windows (mostly-moving + 1–2 stray still samples): old logic accepted them; fixed logic correctly rejects them.

**Practical note (still_fraction):** Passing `min_still ≥ 0.70` means the raw window was *mostly* still, not motion-free for every sample. Edge motion can still pass the gate — consecutive-clean + optical CV checks remain recommended hardening.

## Experimental / limited

| Area | Notes |
|------|--------|
| Glucose accuracy | Depends on volume of high-quality still Libre pairs; not medical grade |
| Hailo HEF models | Pipeline ready; needs trained + DFC-compiled HEF on device |
| Motion artifact rejection on PPG | Basic magnitude gate only |
| SpO₂ during heavy motion | Often invalid (`-1`) by design |

## Recommended next priorities

From armband-ai hardening list (highest leverage first):

1. Consecutive-clean streak in quality / calibration pairing
2. Drift monitor (still-only `filt940` median vs last cal)
3. Tighter optical CV / range / slope thresholds
4. More still Libre pairs → retrain multi-feature and optional MLP
5. Compile and deploy a real HEF once pair count is solid

Firmware-side polish:

- Confirm deep-sleep current with a meter
- Tune INT1 / software motion thresholds on-body
- Decide long-term OLED keep vs remove for battery

## Disclaimer

Experimental personal research. **Not a medical device.**
