# BGM – Wearable Blood Glucose Monitor (Experimental)

**Personal experimental wearable for continuous optical sensing + edge AI glucose estimation.**

> ⚠️ **Not a medical device.** All glucose estimates are experimental research only and must not be used for treatment decisions.

BGM is the **umbrella project** that ties together the wearable firmware and the Pi 5 + Hailo edge-AI host.

| Component | Repository | Role |
|-----------|------------|------|
| **Wearable firmware** | [armband-ppg-940nm](https://github.com/Fryrocket/armband-ppg-940nm) | ESP32-C3 armband: MAX30102 (HR/SpO₂/temp), LIS3DH motion, experimental **940 nm reflectance**, deep sleep, MQTT |
| **Edge AI + dashboard** | [armband-ai](https://github.com/Fryrocket/armband-ai) | Raspberry Pi 5 + Hailo-8: MQTT logger, SQLite, quality gates, CPU + Hailo inference, Streamlit dashboard, Libre calibration |

```
                    ┌──────────────────────────┐
                    │     BGM (this repo)      │
                    │  Umbrella / docs / scripts│
                    └────────────┬─────────────┘
                                 │
          ┌──────────────────────┴──────────────────────┐
          ▼                                             ▼
┌─────────────────────┐                     ┌─────────────────────┐
│ armband-ppg-940nm   │                     │    armband-ai       │
│  (firmware)         │        MQTT         │  (Pi 5 + Hailo)     │
│                     │ ──────────────────► │                     │
│ • XIAO ESP32-C3     │     armband/ppg     │ • Logger + SQLite   │
│ • MAX30102          │                     │ • Quality gates     │
│ • LIS3DH + INT1     │                     │ • Features + models │
│ • 940 nm channel    │                     │ • Hailo-8 HEF       │
│ • Deep sleep        │                     │ • Streamlit dash    │
│ • Battery + OLED    │                     │ • Libre calibration │
└─────────────────────┘                     └─────────────────────┘
```

## Quick start (full system)

```bash
# Clone the umbrella + both component repos into one workspace
git clone https://github.com/Fryrocket/BGM.git
cd BGM
bash scripts/clone-all.sh
```

This creates:

```
BGM/
├── README.md
├── docs/
├── scripts/
├── firmware/          → clone of armband-ppg-940nm
└── host/              → clone of armband-ai
```

Then follow **[docs/SETUP_FULL.md](docs/SETUP_FULL.md)** for hardware, firmware flash, Pi setup, and first calibration.

### Individual repos (if you prefer separate clones)

```bash
git clone https://github.com/Fryrocket/armband-ppg-940nm.git
git clone https://github.com/Fryrocket/armband-ai.git
```

## Documentation

| Doc | Purpose |
|-----|---------|
| **[docs/PINOUT.md](docs/PINOUT.md)** | **Printable pinout + wire color card** (MCU soldering reference) |
| **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** | System architecture, data flow, MQTT contract, feature vector |
| **[docs/SETUP_FULL.md](docs/SETUP_FULL.md)** | End-to-end setup: armband + Pi + Hailo + first readings |
| **[docs/COMPONENTS.md](docs/COMPONENTS.md)** | What lives in each repo and how they talk |
| **[docs/STATUS.md](docs/STATUS.md)** | Current status matrix and open work |
| [armband-ppg-940nm/SETUP.md](https://github.com/Fryrocket/armband-ppg-940nm/blob/main/SETUP.md) | Firmware hardware + flash details |
| [armband-ppg-940nm/PINOUT.md](https://github.com/Fryrocket/armband-ppg-940nm/blob/main/PINOUT.md) | Canonical pinout card (same content) |
| [armband-ai/HARDWARE.md](https://github.com/Fryrocket/armband-ai/blob/main/HARDWARE.md) | Pi 5 + AI HAT + SSD BOM |
| [armband-ai/docs/HAILO_MODEL.md](https://github.com/Fryrocket/armband-ai/blob/main/docs/HAILO_MODEL.md) | Train MLP → ONNX → HEF |

## High-level data flow

1. Armband wakes (timer or LIS3DH INT1), samples sensors, publishes JSON on MQTT topic `armband/ppg`.
2. Pi logger stores readings in SQLite.
3. Feature extraction + quality scoring (still fraction, optical stability, consecutive clean streak).
4. Calibration pairs logged against FreeStyle Libre / fingerstick.
5. CPU models (baseline + multi-feature) run continuously; optional Hailo-8 HEF for neural inference.
6. Live Streamlit dashboard shows readings, quality, estimates, and calibration status.

## Project status (Aug 2026)

| Area | Status |
|------|--------|
| Armband firmware (HR, SpO₂, motion, 940 nm, deep sleep) | Working |
| MQTT streaming + RTC state | Working |
| Pi logger + SQLite + dashboard | Working |
| Quality gates + multi-feature CPU models | Working |
| Hailo-8 path (driver + HEF inference) | Implemented (v0.4.2) |
| Glucose estimation accuracy | Experimental – needs more high-quality still pairs |

See **[docs/STATUS.md](docs/STATUS.md)** for details and next priorities.

## License / disclaimer

Experimental personal research project. See [LICENSE](LICENSE).

**Do not use for medical decisions.**

---

*BGM ties the wearable sensing layer and the edge-AI processing layer into one coherent system.*
