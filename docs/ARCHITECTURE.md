# BGM Architecture

## System overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              BGM System                                     │
│                                                                             │
│  ┌──────────────────────┐         MQTT          ┌─────────────────────────┐ │
│  │  Wearable (ESP32-C3) │  ──────────────────►  │  Host (Raspberry Pi 5)  │ │
│  │  armband-ppg-940nm   │     topic:            │  armband-ai             │ │
│  │                      │     armband/ppg       │                         │ │
│  │  Sensors             │                       │  • Mosquitto broker     │ │
│  │  • MAX30102 PPG      │                       │  • MQTT logger          │ │
│  │  • LIS3DH IMU        │                       │  • SQLite DB            │ │
│  │  • 940 nm optical    │                       │  • Feature extraction   │ │
│  │  • Battery ADC       │                       │  • Quality gates        │ │
│  │                      │                       │  • CPU models           │ │
│  │  Power               │                       │  • Hailo-8 NPU (HEF)    │ │
│  │  • Deep sleep        │                       │  • Streamlit dashboard  │ │
│  │  • INT1 motion wake  │                       │  • Libre calibration    │ │
│  └──────────────────────┘                       └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

## MQTT contract

**Topic:** `armband/ppg`

**QoS:** Firmware publishes with **QoS 0** (PubSubClient default — intentional fire-and-forget for non-critical telemetry). The host logger subscribes at **QoS 1**. Messages can silently drop under poor Wi‑Fi; that is expected until you edit the firmware `publish()` call to QoS 1.

**Payload (JSON) from firmware:**

```json
{
  "bpm": 72,
  "spo2": 98,
  "temp": 36.5,
  "motion": 10.2,
  "moving": false,
  "raw940": 1842,
  "filt940": 1835.4,
  "batt": 3.87,
  "trans": "none",
  "conn_ms": 1240,
  "boot": 42
}
```

| Field | Type | Notes |
|-------|------|-------|
| `bpm` | int | Heart rate; may be 0 when no finger |
| `spo2` | int | SpO₂ %; **-1** means invalid / not computed |
| `temp` | float | Sensor temperature °C |
| `motion` | float | Filtered accel magnitude |
| `moving` | bool | Hysteresis motion flag |
| `raw940` / `filt940` | int / float | 940 nm reflectance (experimental glucose signal) |
| `batt` | float | Battery voltage |
| `trans` | string | `still_to_moving` / `moving_to_still` / `none` |
| `conn_ms` | int | WiFi + MQTT connect time this wake |
| `boot` | int | RTC boot counter |

The Pi logger (`armband_ai.logger`) JSON-parses this and inserts into SQLite. Downstream feature and quality code expect these keys.

## Feature vector (frozen contract)

Used by multi-feature models and the Hailo MLP path. Order must match train → ONNX → HEF:

```
0  filt940_mean
1  filt940_std
2  filt940_min
3  filt940_max
4  filt940_slope
5  raw940_mean
6  bpm_mean
7  bpm_std
8  spo2_mean
9  temp_mean
10 motion_mean
11 motion_max
12 still_fraction
13 moving_transitions
14 batt_mean
15 n_samples
16 duration_s
```

Shape: `[1, 17]` float32.

Extra diagnostic fields on `WindowFeatures` (not in the frozen vector): `max_clean_streak`, `clean_fraction`.

## Inference priority (host)

1. **Hailo HEF** (if configured and device healthy)
2. CPU multi-feature OLS
3. CPU baseline
4. Quality-only (no glucose estimate)

## Quality gates (calibration)

Before a Libre/fingerstick pair enters a model:

- `min_quality` (heuristic 0–100) — recommend ≥ 60–65
- `min_still_fraction` — recommend ≥ 0.70
- `min_clean_streak` — consecutive still **and** optically stable samples; recommend 10–15 (0 = disabled)
- Optical CV / range / slope checks on `filt940`

Drift monitoring (still-only rolling median of `filt940` vs last successful calibration) is recommended but not yet automated.

## Repo boundaries

| Concern | Lives in |
|---------|----------|
| Firmware, pins, deep sleep, sensor drivers | `armband-ppg-940nm` |
| MQTT payload shape (publisher) | `armband-ppg-940nm` |
| MQTT subscriber, DB schema, features, models, Hailo, dashboard | `armband-ai` |
| System docs, clone scripts, architecture | **BGM** (this repo) |

Keep the two component repos independently buildable. BGM only orchestrates and documents.
