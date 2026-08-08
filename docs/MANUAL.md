# BGM Illustrated User Manual

| Document | Description |
|----------|-------------|
| **[BGM_User_Manual.pdf](BGM_User_Manual.pdf)** | Full illustrated step-by-step manual |
| **[BGM_Soldering_Cheat_Sheet.pdf](BGM_Soldering_Cheat_Sheet.pdf)** | One-page printable pinout + soldering order |

> If PDF links 404 on clone, download and place in `docs/`:
> - [BGM_User_Manual.pdf](https://drive.google.com/file/d/1WXUtUwpm-_B4p0XxQ89aXaOqWYHRuLGZ/view)
> - [BGM_Soldering_Cheat_Sheet.pdf](https://drive.google.com/file/d/1-3Mp0HuD2vnVI2Nu498CMh9ydWibN5CD/view)
>
> `git add docs/*.pdf && git commit -m "docs: add illustrated manuals" && git push`

## Document pin (manual generation)

| Repo | Commit (short) |
|------|----------------|
| BGM | `121ca3fbde` |
| armband-ppg-940nm | `87bf9cff26` |
| armband-ai | `1a80ac12c7` |

Generated **2026-08-08**. Re-check SHAs if repos have moved on.

## Manual contents

1. What is BGM?
2. Safety & critical rules
3. System architecture (+ MQTT LAN risk callout)
4. Parts, **tools & consumables**
5. Wearable wiring & soldering (**OLED on shared I2C**, BATTERY_SCALE procedure)
6. **Skin / wear guidance** (placement, tension, calibration hygiene)
7. Firmware setup & first flash
8. Raspberry Pi host setup
9. First data, dashboard & calibration
10. Verification checklist
11. **Production settings — exact revert checklist**
12. Troubleshooting
- Appendix A — I2C scanner
- Appendix B — INT1 / motion tuning
- Appendix C — Deep-sleep current **& battery life estimates**
- Appendix D — **Glossary**
- Companion: `BGM_Soldering_Cheat_Sheet.pdf`

## Practical callouts

### still_fraction
Passing `min_still ≥ 0.70` means the **raw window was mostly still**, not motion-free for every sample. Consecutive-clean + optical CV remain recommended.

### Latched INT1
Clear via `INT1_SRC` on wake and before sleep. ESP32-C3 uses `esp_deep_sleep_enable_gpio_wakeup` only (no ext0/ext1).

### MQTT
Empty user/password is allowed for bring-up. Prefer local broker auth; do not expose to the public internet. Default path is cleartext on the LAN (biometric telemetry).

### OLED
Optional SSD1306 shares **D4/D5 I2C** + 3V3 + GND — no extra GPIO. Listed in pin map and soldering step 8.

**Experimental research only. Not a medical device.**  
Copyright (C) 2026 Fryrocket · GNU GPLv3 or later
