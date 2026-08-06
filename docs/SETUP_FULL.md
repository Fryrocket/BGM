# Full System Setup (BGM)

End-to-end path from empty desk to streaming armband + live dashboard.

## 0. Clone workspace

```bash
git clone https://github.com/Fryrocket/BGM.git
cd BGM
bash scripts/clone-all.sh
```

Result:

```
BGM/
├── firmware/   # armband-ppg-940nm
└── host/       # armband-ai
```

Or clone the three repos as siblings if you prefer.

## 1. Hardware checklist

### Wearable (firmware)

- Seeed XIAO ESP32-C3
- MAX30102
- LIS3DH (INT1 → XIAO D2)
- TSAL6200 + BPW34 (940 nm channel)
- 3.7 V ~500 mAh LiPo + JST
- Elastic armband mount

Details: [armband-ppg-940nm SETUP.md](https://github.com/Fryrocket/armband-ppg-940nm/blob/main/SETUP.md)

### Host (Pi)

- Raspberry Pi 5 (4/8 GB)
- Official 27 W PSU
- ~250 GB SSD (boot drive recommended)
- Raspberry Pi AI HAT+ (Hailo-8, 26 TOPS preferred)
- Active cooler
- Same Wi-Fi/LAN as armband

Details: [armband-ai HARDWARE.md](https://github.com/Fryrocket/armband-ai/blob/main/HARDWARE.md)

### Reference

- FreeStyle Libre or fingerstick meter for calibration labels

## 2. Firmware

1. Open `firmware/firmware/Armband_Full.ino` (after clone-all) or the file in the standalone repo.
2. Edit **USER CONFIG**:
   - `WIFI_SSID` / `WIFI_PASSWORD`
   - `MQTT_SERVER` = Pi IP address
   - `MQTT_USER` / `MQTT_PASSWORD` (or empty)
   - Battery scale if needed
3. Flash via Arduino IDE (board: Seeed XIAO ESP32C3) or PlatformIO.
4. Serial monitor @ 115200: confirm wake → publish → deep sleep cycle.

MQTT topic must remain **`armband/ppg`** unless you change both sides.

## 3. Pi host

```bash
cd host   # or ~/armband-ai

# System packages
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y mosquitto mosquitto-clients dkms hailo-all zstd
# reboot after hailo-all

# Python env
python3 -m venv .venv --system-site-packages
source .venv/bin/activate
pip install -r requirements.txt

cp -n config.example.yaml config.yaml
# Edit config.yaml: mqtt credentials if used, paths if non-default

# Verify Hailo (optional but recommended)
hailortcli fw-control identify
python scripts/hailo_diagnose.py
```

Start services:

```bash
python scripts/run_logger.py &
python scripts/run_inference.py &
bash scripts/run_dashboard.sh
```

Or install systemd units from `host/systemd/`.

## 4. First data

1. Wear armband, stay relatively still for a minute.
2. Confirm logger prints incoming messages (`bpm`, `filt940`, etc.).
3. Open the Streamlit dashboard (default port from `run_dashboard.sh`).
4. Log a Libre reading while still:

```bash
python scripts/log_glucose.py 142 --notes "still"
```

5. After several high-quality pairs:

```bash
python scripts/calibrate.py --min-quality 60 --min-still 0.7
python scripts/train_multifeature.py --min-quality 60
```

Optional neural path: see [HAILO_MODEL.md](https://github.com/Fryrocket/armband-ai/blob/main/docs/HAILO_MODEL.md).

## 5. Verification checklist

- [ ] Armband publishes on `armband/ppg`
- [ ] Pi logger stores rows in SQLite
- [ ] Dashboard live tab updates
- [ ] `spo2` of -1 is treated as invalid (not averaged as zero)
- [ ] Still periods produce higher quality scores
- [ ] (Optional) `hailortcli` reports HAILO8 and diagnose is HEALTHY

## Troubleshooting pointers

| Symptom | Where to look |
|---------|----------------|
| No MQTT messages | Firmware USER CONFIG (IP, topic, WiFi); Mosquitto on Pi |
| Logger errors on payload | JSON field names vs `db.insert_reading` |
| Poor calibration | Still time, quality gates, contact consistency |
| Hailo not ready | `docs/HAILO_DRIVER.md` in armband-ai |

---

For component-specific deep dives, stay in the individual repos. This doc only covers the integrated path.
