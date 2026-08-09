# S001 — Plumbing Verification Checklist

**Purpose:** prove the pipeline carries a real number end to end. Not a calibration session. No Libre required.  
**Duration:** ~30 min · **Prereq:** band fitted, Pi up, phone on same network  
**Status:** Approved by Grok (PM) 2026-08-09 — run before S002.

Record result as PASS / FAIL / SKIP. A FAIL stops the session — note it and fix before S002.

---

## Firmware → MQTT

- [ ] **1. Boot.** Serial shows `LIS3DH OK` with an address, `MAX30102 OK`, and `INT1 configured`. — FAIL if any sensor reports not found.
- [ ] **2. Publish.** `mosquitto_sub -t armband/ppg -v` on the Pi shows JSON arriving. — PASS: well-formed JSON, all 11 fields present.
- [ ] **3. 940 nm is alive.** `raw940` and `filt940` change between publishes and sit away from 0 and from the ADC rail (4095). — FAIL if flat, pinned, or identical across three consecutive messages. *Everything downstream is decorative if this fails.*
- [ ] **4. Sentinels.** With no finger on the sensor, `bpm` and `spo2` report −1 rather than 0.
- [ ] **5. Battery.** `batt` is plausible for a charged LiPo (roughly 3.7–4.2 V).
- [ ] **6. Motion wake.** Move the arm sharply. — PASS: wake within ~1 s, GPIO wake, genuine `trans`.
- [ ] **7. Quiet wake.** Two full 3-minute timer cycles. Quiet-skip behaves; records still arrive.

## Pi → storage

- [ ] **8. Rows landing.** SQLite row count increases.
- [ ] **9. Soft validation.** No clamp/reject spam for normal readings.
- [ ] **10. Features compute.** Quality scores on real windows.
- [ ] **11. Clean streak moves.** Non-zero during still period.

## Dashboard

- [ ] **12. Live tab.** Session visible, plotting, no stack traces.
- [ ] **13. Quality visible.** Score varies with movement.
- [ ] **14. Drift section renders** (no baseline yet — OK).

## Phone

- [ ] **15. Receives.** Live tab + pending count climbs.
- [ ] **16. Dump to Pi.** ACK; pending → 0.
- [ ] **17. Partial insert.** Re-dump; green; `inserted + duplicates >= count`.
- [ ] **18. Cancel mid-dump.** No red; partial credit OK.
- [ ] **19. Cancel after success.** `totalSynced` does not drop.
- [ ] **20. Manual disconnect.** Silent settle, no red UI.

## Export

- [ ] **21. Export path works.** File appears under `04_Logs_Exports/`.

---

## Session Log stub

```
Session_ID:        S001
Band_Placement_ID: P01
Num_Libre_Pairs:   0
Num_Fingerstick:   0
Model_Version:     none
Notes:             S001 plumbing. Checklist __/21. Failures: ____
```

**Read-out:** 21/21 → S002 may chase glucose. Less → fix plumbing first.

Experimental research only — not a medical device.
