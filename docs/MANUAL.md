# BGM Illustrated User Manual

Printed / PDF guides for the full system.

| Document | Description |
|----------|-------------|
| **[BGM_User_Manual.pdf](BGM_User_Manual.pdf)** | Full illustrated step-by-step manual (wiring, firmware, Pi host, calibration, appendices) |
| **[BGM_Soldering_Cheat_Sheet.pdf](BGM_Soldering_Cheat_Sheet.pdf)** | One-page printable pinout + wire colors + soldering order |

> **Note:** If the PDF links above 404 on a fresh clone, download from Google Drive and place them in `docs/`:
> - [BGM_User_Manual.pdf](https://drive.google.com/file/d/1qOg_rRg8EGSbF83JS6pWgIZFoRkgCJAy/view)
> - [BGM_Soldering_Cheat_Sheet.pdf](https://drive.google.com/file/d/1-3Mp0HuD2vnVI2Nu498CMh9ydWibN5CD/view)
>
> Then: `git add docs/*.pdf && git commit -m "docs: add illustrated manuals" && git push`

Also see:

- [PINOUT.md](PINOUT.md) — canonical pinout card (markdown)
- [SETUP_FULL.md](SETUP_FULL.md) — end-to-end text setup
- [ARCHITECTURE.md](ARCHITECTURE.md) — MQTT contract + feature vector
- [STATUS.md](STATUS.md) — current status matrix

## Manual contents (PDF)

1. What is BGM?
2. Safety & disclaimer (LiPo → battery pads only)
3. System architecture
4. Parts checklist
5. Wearable wiring & soldering
6. Firmware setup & first flash
7. Raspberry Pi host setup
8. First data, dashboard & calibration
9. Verification checklist
10. Troubleshooting
11. Production settings & next steps
- Appendix A — I²C scanner
- Appendix B — INT1 / motion tuning on-body
- Appendix C — Measuring deep-sleep current

**Experimental research only. Not a medical device.**  
Copyright (C) 2026 Fryrocket · GNU GPLv3 or later
