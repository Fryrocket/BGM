# BGM Components

## Repository map

| Repo | Path after `clone-all.sh` | Primary language | Responsibility |
|------|---------------------------|------------------|----------------|
| **BGM** | `.` | Markdown / shell | Umbrella docs, architecture, workspace scripts |
| **armband-ppg-940nm** | `firmware/` | C++ (Arduino / PlatformIO) | Wearable firmware, sensors, MQTT publish, power |
| **armband-ai** | `host/` | Python | MQTT consume, DB, features, models, Hailo, dashboard |

## armband-ppg-940nm (firmware)

**Owns:**

- Pin map and sensor drivers (MAX30102, LIS3DH, 940 nm, battery ADC, OLED)
- Deep sleep + INT1 motion wake + RTC state
- MQTT publisher (topic `armband/ppg`, JSON schema above)
- On-device filtering (EMA motion, EMA 940 nm)

**Does not own:**

- Storage, models, UI, calibration math

Key entry: `firmware/Armband_Full.ino`  
Docs: `SETUP.md`, `NOTES.md`

## armband-ai (host)

**Owns:**

- MQTT subscriber and SQLite schema
- Window features and quality scoring
- Baseline / multi-feature training and inference
- Hailo driver helpers and HEF runner
- Streamlit dashboard
- Libre logging and calibration pipelines
- systemd units and log rotation

**Does not own:**

- Firmware source or armband pinout (referenced only)

Key entry points:

- `scripts/run_logger.py`
- `scripts/run_inference.py`
- `scripts/run_dashboard.sh`
- `src/armband_ai/`

Docs: `HARDWARE.md`, `docs/HAILO_*.md`, `docs/PIPELINE.md`, `docs/LIBRE_FLOW.md`

## BGM (this repo)

**Owns:**

- Single place that describes how the two halves form one system
- Clone / workspace scripts
- Cross-cutting architecture and status

**Does not** vendor large copies of firmware or host code (use clones or, later, true git submodules if desired).

## Communication boundary

The only runtime coupling is **MQTT topic + JSON fields**.  
Change the topic or field names on **both** sides or the link breaks.

Config alignment checklist:

| Firmware | Host (`config.yaml`) |
|----------|----------------------|
| `MQTT_TOPIC = "armband/ppg"` | `mqtt.topic: "armband/ppg"` |
| `MQTT_SERVER` = Pi IP | broker usually `localhost` on Pi |
| user/pass (optional) | matching `mqtt.username` / `password` |

## Optional: true git submodules

If you want the component repos tracked as submodules instead of sibling clones:

```bash
cd BGM
git submodule add https://github.com/Fryrocket/armband-ppg-940nm.git firmware
git submodule add https://github.com/Fryrocket/armband-ai.git host
git commit -m "Add firmware and host as submodules"
```

Then clones of BGM need:

```bash
git clone --recurse-submodules https://github.com/Fryrocket/BGM.git
# or after clone:
git submodule update --init --recursive
```

The provided `scripts/clone-all.sh` uses plain clones (simpler for day-to-day dual-repo work). Switch to submodules when you want a single pinned workspace commit.
