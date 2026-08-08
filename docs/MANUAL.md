# BGM Illustrated User Manual

Printed / PDF guides for the full system.

| Document | Description |
|----------|-------------|
| **[BGM_User_Manual.pdf](BGM_User_Manual.pdf)** | Full illustrated step-by-step manual (wiring, firmware, Pi host, calibration, appendices) |
| **[BGM_Soldering_Cheat_Sheet.pdf](BGM_Soldering_Cheat_Sheet.pdf)** | One-page printable pinout + wire colors + soldering order |

> **Note:** If the PDF links above 404 on a fresh clone, download and place them in `docs/`:
> - [BGM_User_Manual.pdf](https://drive.google.com/file/d/1pRCCOmHapwTVkaBosoUSfZWLxVAIIN9w/view) (updated with callouts)
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

## Practical callouts (also in the PDF)

### Calibration — still_fraction

`still_fraction` is computed on the **raw window before** prefer-still filtering (so the gate is not trivially 1.0). Passing `min_still ≥ 0.70` means the window was **mostly still**, not motion-free for every sample. A few seconds of motion at the edge of a window can still pass. Do not treat “passed quality gate” as proof the session was clean end-to-end — consecutive-clean streak and optical CV/range checks remain recommended.

### Firmware — latched INT1

LIS3DH INT1 is **active-low and latched**. Once it fires, it stays asserted until firmware reads `INT1_SRC`. If that clear never happens, the pin can immediately re-wake the ESP32-C3 or block the next deep sleep. On this chip, GPIO wake uses `esp_deep_sleep_enable_gpio_wakeup` (not ext0/ext1 — those sources do not exist on ESP32-C3). Always clear the latch on wake and again before re-entering sleep.

**Experimental research only. Not a medical device.**  
Copyright (C) 2026 Fryrocket · GNU GPLv3 or later
