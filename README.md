# BGM – Wearable Blood Glucose Monitor (Experimental)

**Personal experimental wearable for continuous optical sensing + edge AI glucose estimation.**

> ⚠️ **Not a medical device.** All glucose estimates are experimental research only and must not be used for treatment decisions.

BGM is the **umbrella project** that ties together the wearable firmware, the Pi 5 + Hailo edge-AI host, and the new iOS companion app.

| Component | Repository | Role |
|-----------|------------|------|
| **Wearable firmware** | [armband-ppg-940nm](https://github.com/Fryrocket/armband-ppg-940nm) | ESP32-C3 armband: MAX30102 (HR/SpO₂/temp), LIS3DH motion, experimental **940 nm reflectance**, deep sleep, MQTT |
| **Edge AI + dashboard** | [armband-ai](https://github.com/Fryrocket/armband-ai) | Raspberry Pi 5 + Hailo-8: MQTT logger, SQLite, quality gates, CPU + Hailo inference, Streamlit dashboard, Libre calibration |
| **iOS companion** | [armband-ios](https://github.com/Fryrocket/armband-ios) | iPhone app: live graphs, offline storage, BLE/MQTT, dump-to-Pi when connection returns |

```
                    ┌──────────────────────────┐
                    │     BGM (this repo)      │
                    │  Umbrella / docs / scripts│
                    └────────────┬─────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          ▼                      ▼                      ▼
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│ armband-ppg-940nm   │  │    armband-ai       │  │   armband-ios       │
│  (firmware)         │  │  (Pi 5 + Hailo)     │  │  (iPhone companion) │
│                     │  │                     │  │                     │
│ • XIAO ESP32-C3     │  │ • Logger + SQLite   │  │ • Live graphs       │
│ • MAX30102          │  │ • Quality gates     │  │ • Offline store     │
│ • LIS3DH + INT1     │  │ • Features + models │  │ • BLE / MQTT        │
│ • 940 nm channel    │  │ • Hailo-8 HEF       │  │ • Dump to Pi        │
│ • Deep sleep        │  │ • Streamlit dash    │  │ • Session recording │
│ • Battery + OLED    │  │ • Libre calibration │  │                     │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
```

## Quick start (full system)

```bash
# Clone the umbrella + component repos into one workspace
git clone https://github.com/Fryrocket/BGM.git
cd BGM
bash scripts/clone-all.sh
```

Then follow **[docs/BGM_User_Manual.pdf](docs/BGM_User_Manual.pdf)** or **[docs/SETUP_FULL.md](docs/SETUP_FULL.md)**.

### Individual repos

```bash
git clone https://github.com/Fryrocket/armband-ppg-940nm.git
git clone https://github.com/Fryrocket/armband-ai.git
git clone https://github.com/Fryrocket/armband-ios.git
```

## Documentation

| Doc | Purpose |
|-----|---------|
| **[docs/BGM_User_Manual.pdf](docs/BGM_User_Manual.pdf)** | Illustrated step-by-step user manual |
| **[docs/BGM_Soldering_Cheat_Sheet.pdf](docs/BGM_Soldering_Cheat_Sheet.pdf)** | Printable soldering / pinout card |
| **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** | System architecture, data flow, MQTT contract |
| **[docs/SETUP_FULL.md](docs/SETUP_FULL.md)** | End-to-end setup |
| **[docs/STATUS.md](docs/STATUS.md)** | Current status matrix |
| **[docs/S001_Run_Sheet.md](docs/S001_Run_Sheet.md)** | S001 plumbing verification (one-page run sheet) |
| [armband-ios/README.md](https://github.com/Fryrocket/armband-ios) | iOS companion app status & plans |

## High-level data flow

1. Armband wakes, samples sensors, publishes JSON (MQTT or BLE).
2. Data can go directly to Pi **or** to iPhone (offline store).
3. iPhone dumps stored batches to Pi when connection is available.
4. Pi logger → SQLite → quality gates → models → Streamlit dashboard.
5. Calibration pairs logged against FreeStyle Libre / fingerstick.

## Project status (Aug 2026)

| Area | Status |
|------|--------|
| Armband firmware | Working |
| MQTT streaming | Working |
| Pi logger + dashboard | Working |
| Quality gates + models | Implemented (zero real pairs; n≤p refusal active) |
| Hailo-8 path | Implemented |
| **iOS companion app** | **Scaffolded (new)** |
| Glucose estimation accuracy | Experimental |

## File index

**Docs**
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — system architecture, feature vector + MQTT contracts
- [docs/BGM_Core_Dump_Refresh_2026-08-09_PM.md](docs/BGM_Core_Dump_Refresh_2026-08-09_PM.md)
- [docs/COMPONENTS.md](docs/COMPONENTS.md) — hardware bill of materials
- [docs/MANUAL.md](docs/MANUAL.md) — user manual
- [docs/PINOUT.md](docs/PINOUT.md) — wiring and pin assignments
- [docs/S001_Plumbing_Verification_Checklist.md](docs/S001_Plumbing_Verification_Checklist.md)
- [docs/S001_Run_Sheet.md](docs/S001_Run_Sheet.md)
- [docs/SETUP_FULL.md](docs/SETUP_FULL.md) — end-to-end setup path
- [docs/STATUS.md](docs/STATUS.md) — current project status
- [docs/automation/bgm-bundle-repos.sh](docs/automation/bgm-bundle-repos.sh)
- [docs/automation/bgm-drive-backup.service](docs/automation/bgm-drive-backup.service)
- [docs/automation/bgm-drive-backup.timer](docs/automation/bgm-drive-backup.timer)
- [docs/automation/bgm-drive-snapshot.sh](docs/automation/bgm-drive-snapshot.sh)
- [docs/automation/rclone_bgm_backup.md](docs/automation/rclone_bgm_backup.md)
- [docs/desk/CHECKLIST.md](docs/desk/CHECKLIST.md)
- [docs/desk/INBOX/T001-claude.md](docs/desk/INBOX/T001-claude.md)
- [docs/desk/INBOX/T002-gemini.md](docs/desk/INBOX/T002-gemini.md)
- [docs/desk/NOTES.md](docs/desk/NOTES.md)
- [docs/desk/PROTOCOL.md](docs/desk/PROTOCOL.md)
- [docs/desk/START_HERE.md](docs/desk/START_HERE.md)

**Scripts**
- [scripts/clone-all.sh](scripts/clone-all.sh) — clone all component repos into one workspace
- [scripts/generate_changelog.py](scripts/generate_changelog.py)
- [scripts/generate_file_indexes.py](scripts/generate_file_indexes.py) — regenerate File index sections across all component READMEs
- [scripts/generate_notes.py](scripts/generate_notes.py)
- [scripts/setup-workspace.sh](scripts/setup-workspace.sh) — workspace helper
- [scripts/update_file_index.py](scripts/update_file_index.py) — single-repo File index updater used by GitHub Action

**Config**
- [.gitignore](.gitignore)
- [LICENSE](LICENSE)

## License / disclaimer

**GNU General Public License v3.0 or later**.  
Experimental personal research project. **Do not use for medical decisions.**
