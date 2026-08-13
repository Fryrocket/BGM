# BGM Status (2026-08-13 13:15 CDT)

Pickup. Last wrist contact: **2026-08-09**. No S001 measurement.

## armband-ai HEAD (work today)

See [armband-ai/docs/STATUS.md](https://github.com/Fryrocket/armband-ai/blob/main/docs/STATUS.md) for the live pickup.

Today: disabled Hailo/MLP (1121 params), three-condition hard gate (bpm / spo2 / motion), baseline is the only S001 path and now refuses mixed subjects, n<10, tight/bimodal glucose.

| SHA (human) | What |
|-------------|------|
| *(armband-ai main)* | ASK 21 amend + ASK 24 drop-count sidecar |
| `a63cae7` | ASK 20–23 |
| `d042baa` | ASK 16–19 |
| `2978112` `7cb852f` `85f8af3` | v0.5.1 disable + gate |

Package **0.5.1**. Other repos unchanged: BGM `3a79cef2`, ppg `3a3304fa`, ios `c4af2878`.

## Working

| Area | Notes |
|------|--------|
| Firmware HR / SpO₂ / temp | MAX30102; gated on `maxOk` |
| LIS3DH motion + INT1 wake | Separate chip; missing `moving` is now a **hard gate fail** (`no_motion_data`) |
| 940 nm channel | Multi-sample + EMA; gpio hold; RTC EMA seed flags |
| MQTT + SQLite | Continuous ingest; per-reading `session_id` |
| Feature extraction | Frozen **17-vector** (`filt940_std` in contract). `n_valid_*` are gate-side only. |
| Quality gate | Hard-fail: `no_valid_bpm`, `no_valid_spo2`, `no_motion_data`. Soft heuristics after. |
| Hailo / MLP | **DISABLED** until per-subject pairs are four figures. `_param_count()` derived. |
| Multi-feature OLS | n ≤ p bar (p=10). Will not run at S001. |
| **Baseline** | **The S001 path.** Mixed subjects raise. n≥10. Range≥40 **and** 3 terciles. n<30 → `grade=pilot`. |
| Drop counts | `.attrs` + sibling `*.csv.drops.json` (`write_pairs`). Band-fit diagnostic. |
| Streamlit dashboard | Shows drop counts and pilot-grade warning. |
| iOS companion | Unchanged today. |

## Locked decisions (2026-08-11 / 12)

See Drive **BGM_Decisions_2026-08-12**.

1. Re-seat = new session.
2. Homogeneity — mixed session_id in a window → `dropped_mixed_session`.
3. Per-subject fits only — never pool. `fit_baseline` now **raises** on mixed subjects.
4. Schema freeze.
5. Armband_Temp = MAX30102 die temperature (in the frozen 17-vector; hold-back is a product call, not a code defect).
6. Export protocol — dated CSV in `02_Calibration_Data`.

Live sheet IDs:
- Tracker: `17uJJ6bp2dJ9GLERNZFdbtL8_NxvoEfWclgX8TFe5n-w`
- Session Log: `1Jh0geyD5ETSlHHeoTT5A8eONzx44hiOT77aTF9q2zBc`

## Open

| ID | Item |
|----|------|
| 1 | **S001 / source population** — main event. Band not on a wrist. |
| 6 | `filt940_std` → `sd` at sheet-write boundary only. |
| 4 | Hailo provenance — deprioritised (path off). |
| 15 | Drive write from implementer is intermittent. Snapshot `08_Source_Snapshot/2026-08-13` cut at armband-ai `794019d2` is **stale**. |

## Experiment status

| Folder / sheet | State |
|----------------|--------|
| Calibration / models / logs / photos | **Empty** — gates ahead of data |
| Tracker / Session Log | Headers only; schema frozen |
| **Next** | **S001 plumbing** — Run Sheet ready |

## Disclaimer

Experimental personal research. **Not a medical device**.
