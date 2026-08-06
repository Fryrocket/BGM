#!/usr/bin/env bash
# Convenience: clone components + print next steps.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

bash scripts/clone-all.sh

echo
echo "=== BGM workspace ==="
echo "Firmware:  $ROOT/firmware"
echo "Host:      $ROOT/host"
echo
echo "Suggested next steps:"
echo "  1. Edit firmware USER CONFIG (WiFi + MQTT → Pi IP)"
echo "  2. Flash Armband_Full.ino to XIAO ESP32-C3"
echo "  3. On Pi: cd host && follow HARDWARE.md + config.example.yaml"
echo "  4. Start logger / inference / dashboard"
echo "  5. docs/SETUP_FULL.md for the full checklist"
