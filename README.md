# BGM – Wearable Blood Glucose Monitor (Experimental)

**Personal experimental wearable for continuous optical sensing + on-device / edge AI glucose estimation.**

> ⚠️ **Not a medical device.** All glucose estimates are experimental research only and must not be used for treatment decisions.

BGM is the umbrella project that ties together the two specialized repositories:

| Component | Repository | Role |
|-----------|------------|------|
| **Wearable firmware** | [armband-ppg-940nm](https://github.com/Fryrocket/armband-ppg-940nm) | ESP32-C3 armband: MAX30102 (HR/SpO₂/temp), LIS3DH motion, experimental **940 nm reflectance** channel, deep sleep, MQTT streaming |
| **Edge AI + dashboard** | [armband-ai](https://github.com/Fryrocket/armband-ai) | Raspberry Pi 5 + Hailo-8 AI HAT: MQTT logger, SQLite, quality-gated features, CPU models, optional Hailo HEF inference, Streamlit live dashboard, Libre calibration pipeline |

```
                    ┌──────────────────────────┐
                    │     BGM (this repo)     │
                    │   Umbrella / docs hub   │
                    └───────────┬───────────┘
                             │
          ┌─────────────┴─────────────┐
          │                                      │
          ▼                                      ▼
┌──────────────────────┐          ┌──────────────────────┐
│ armband-ppg-940nm │          │   armband-ai      │
│  (firmware)       │          │  (Pi 5 + Hailo)   │
│                   │          │                   │
│ • XIAO ESP32-C3   │   MQTT   │ • Logger + SQLite │
│ • MAX30102        │ ───────▶ │ • Quality gates   │
│ • LIS3DH + INT1   │ armband/ │ • Features + models│
│ • 940 nm channel  │   ppg    │ • Hailo-8 HEF     │
│ • Deep sleep      │          │ • Streamlit dash  │
│ • Battery + OLED  │          │ • Libre calibration│
└──────────────────────┘          └──────────────────────┘
```

## Quick links

- **Firmware (armband)** → [Fryrocket/armband-ppg-940nm](https://github.com/Fryrocket/armband-ppg-940nm)  
  Setup, NOTES, PlatformIO, deep-sleep strategy, 940 nm channel.

- **Edge AI host (Pi 5 + Hailo)** → [Fryrocket/armband-ai](https://github.com/Fryrocket/armband-ai)  
  HARDWARE.md, HAILO_DRIVER.md, HAILO_MODEL.md, quality gates, drift monitoring, dashboard, systemd services.

## High-level data flow

1. Armband wakes (timer or LIS3DH INT1 motion), samples sensors, publishes JSON on MQTT topic `armband/ppg`.
2. Pi logger (`armband-ai`) receives the payload and stores it in SQLite.
3. Feature extraction + quality scoring (still fraction, optical stability, consecutive clean streak).
4. Calibration pairs logged against FreeStyle Libre / fingerstick.
5. CPU models (baseline + multi-feature) run continuously; optional Hailo-8 HEF for neural inference.
6. Live Streamlit dashboard shows readings, quality, estimates, and calibration status.

## Getting started (full system)

1. **Hardware**  
   - Build / flash the armband (see armband-ppg-940nm `SETUP.md`).  
   - Set up Pi 5 + AI HAT+ (Hailo-8) + SSD boot + Mosquitto (see armband-ai `HARDWARE.md`).

2. **Firmware**  
   - Edit `USER CONFIG` in `Armband_Full.ino` (WiFi, MQTT broker = Pi IP, credentials).  
   - Upload and confirm MQTT packets appear.

3. **Pi side**  
   ```bash
   git clone https://github.com/Fryrocket/armband-ai.git
   cd armband-ai
   cp config.example.yaml config.yaml   # edit as needed
   # start logger / inference / dashboard (or enable systemd units)
   ```

4. **Calibration**  
   - Sit still, log Libre readings via `log_glucose.py` or the dashboard.  
   - Run quality-gated calibration and (optionally) train MLP → ONNX → HEF.

## Project status (Aug 2026)

| Area | Status |
|------|--------|
| Armband firmware (HR, SpO₂, motion, 940 nm, deep sleep) | Working |
| MQTT streaming + RTC state | Working |
| Pi logger + SQLite + dashboard | Working |
| Quality gates + multi-feature CPU models | Working |
| Hailo-8 path (driver + HEF inference) | Implemented (v0.4.2) |
| Glucose estimation accuracy | Experimental – needs more high-quality still pairs |

## License / disclaimer

Experimental personal research project.  
**Do not use for medical decisions.**

---

*BGM ties the wearable sensing layer and the edge-AI processing layer into one coherent system.*
