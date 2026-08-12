# S001 Run Sheet — Plumbing Verification

**Purpose:** Prove the pipeline carries a real number end-to-end.  
**Not calibration.** No Libre / fingerstick required. Produces zero pairs.  
**Duration:** ~25–40 min seated.  
**Prereqs:** Band charged + fitted, Pi on same LAN, phone on same network, services up.

**Session Log pre-fill (do this first, before powering the band):**

```
Session_ID:          S001
Subject_ID:          SUBJ_A
Band_Placement_ID:   P001
Start_DateTime:      <fill when you start>
End_DateTime:        <fill when you stop>
Duration_min:        
Still_Minutes:       
Avg_Quality:         
Num_Libre_Pairs:     0
Num_Fingerstick:     0
Notes:               S001 plumbing only. Checklist __/21. Failures: ____
Firmware_Version:    <from serial or app>
Model_Version:       none
```

**Decisions already locked (do not invent mid-session):**
- Subject_ID = SUBJ_A
- Band_Placement_ID = P001 (one placement for the whole run)
- Re-seat ends the session → if you re-seat, close S001 and open S002 with new placement
- No glucose labels
- Export Session Log CSV immediately after the row is filled (habit start)

---

## 0. Pre-flight (2 min)

```bash
# On Pi — confirm services
ps aux | grep -E 'run_logger|run_inference|streamlit' | grep -v grep

# Confirm Mosquitto listening
mosquitto_sub -h localhost -t armband/ppg -v -C 1   # should block until first message or timeout
```

If logger is not running: `cd ~/armband-ai && source .venv/bin/activate && python scripts/run_logger.py &`

---

## 1. Firmware → MQTT (items 1–7)

Power the band. Serial @ 115200:

- [ ] **1.** Boot: `LIS3DH OK` (addr), `MAX30102 OK`, `INT1 configured`
- [ ] **2.** Publish arrives:  
  `mosquitto_sub -t armband/ppg -v`  
  → well-formed JSON, all expected fields present
- [ ] **3.** 940 nm alive: `raw940` / `filt940` change, not 0, not pinned at 4095
- [ ] **4.** Sentinels: no finger → `bpm`/`spo2` = −1
- [ ] **5.** Battery: `batt` ≈ 3.7–4.2 V
- [ ] **6.** Motion wake: sharp arm move → wake ≤1 s, genuine `trans`
- [ ] **7.** Quiet wake: two full timer cycles; quiet-skip works; records still arrive

**Fail-stop:** if #3 fails, stop. Everything downstream is noise.

---

## 2. Pi → storage + features (items 8–11)

```bash
# Row count climbing
sqlite3 ~/armband-ai/data/armband.db "SELECT COUNT(*) FROM readings;"

# Soft validation quiet
# (watch logger stdout — no clamp/reject spam on normal still readings)

# Features / quality visible on dashboard or:
python -c "
from armband_ai.features import features_from_db
from armband_ai.config import load_config
cfg = load_config()
print(features_from_db(cfg['database']['path'], minutes=3))
"
```

- [ ] **8.** SQLite row count increases
- [ ] **9.** No clamp/reject spam for normal readings
- [ ] **10.** Features compute (quality scores on real windows)
- [ ] **11.** Clean streak moves / non-zero during still

---

## 3. Dashboard (items 12–14)

- [ ] **12.** Live tab: session visible, plotting, no stack traces
- [ ] **13.** Quality score varies with movement
- [ ] **14.** Drift section renders (empty baseline is expected / OK)

---

## 4. Phone / iOS (items 15–20)

- [ ] **15.** Receives: Live tab + pending count climbs
- [ ] **16.** Dump to Pi: ACK; pending → 0
- [ ] **17.** Partial insert: re-dump → green; `inserted + duplicates >= count`
- [ ] **18.** Cancel mid-dump: no red; partial credit OK
- [ ] **19.** Cancel after success: `totalSynced` does not drop
- [ ] **20.** Manual disconnect: silent settle, no red UI

---

## 5. Export (item 21) + close

- [ ] **21.** Export works (or at minimum: Session Log CSV written)

**Close the session:**
1. Fill End_DateTime + notes (score out of 21 + any failures).
2. Export both sheets immediately:
   - File → Download → CSV
   - Name: `BGM_Session_Log_S001_YYYY-MM-DD.csv`  
     (Tracker will be empty — still export for habit)
   - Drop into `02_Calibration_Data/Sheet_Snapshots/`
3. Power band down or leave in production quiet-wake.

**Read-out:**  
21/21 → green light for S002 (glucose + re-seat controls).  
Any FAIL → fix plumbing first. Do not proceed to calibration pairs until clean.

---

Experimental research only — **not a medical device**.
