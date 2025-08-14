#!/usr/bin/env python3
"""
monitor.py
Simple monitor that scans device_heartbeats.log and raises alerts when
a device hasn't reported within threshold seconds.

Usage:
  python monitor.py --threshold 12 --scan-interval 5
"""

import time
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

LOG_FILE = Path("device_heartbeats.log")
ALERT_LOG = Path("alerts.log")
ALERT_JSON = Path("alerts.json")

def parse_line(line):
    try:
        obj = json.loads(line)
        ts = datetime.strptime(obj["ts"], "%Y-%m-%dT%H:%M:%SZ")
        return obj["device_id"], ts, obj
    except Exception:
        return None, None, None

def scan_last_seen():
    """
    Parse the entire log and return a dict: device_id -> last_seen_timestamp, last_entry
    (Simple but fine for small logs. For production, we use a persisted DB or file offset.)
    """
    last = {}
    if not LOG_FILE.exists():
        return last

    with LOG_FILE.open("r", encoding="utf-8") as fh:
        for line in fh:
            device_id, ts, obj = parse_line(line.strip())
            if device_id and ts:
                if device_id not in last or ts > last[device_id]["ts"]:
                    last[device_id] = {"ts": ts, "entry": obj}
    return last

def write_alert(device_id, when, reason, details=None):
    alert = {
        "alert_ts": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "device_id": device_id,
        "reason": reason,
        "detected_at": when.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "details": details or {}
    }
    # append human-readable log
    with ALERT_LOG.open("a", encoding="utf-8") as fh:
        fh.write(f"{alert['alert_ts']} ALERT {device_id} {reason} {json.dumps(alert['details'])}\n")
    # update JSON file (overwrite for simplicity)
    alerts = []
    if ALERT_JSON.exists():
        try:
            alerts = json.loads(ALERT_JSON.read_text(encoding="utf-8"))
        except Exception:
            alerts = []
    alerts.append(alert)
    ALERT_JSON.write_text(json.dumps(alerts, indent=2), encoding="utf-8")
    print(f"[monitor] ALERT -> {device_id} {reason}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=int, default=12, help="Missing-heartbeat threshold in seconds")
    parser.add_argument("--scan-interval", type=int, default=5, help="How often monitor checks the log (seconds)")
    args = parser.parse_args()

    print(f"Monitor started: threshold={args.threshold}s scan_interval={args.scan_interval}s")
    try:
        while True:
            last_seen = scan_last_seen()
            now = datetime.utcnow()
            # For demo: assume known small set of devices - pick from last_seen keys
            for device_id, info in last_seen.items():
                delta = (now - info["ts"]).total_seconds()
                if delta > args.threshold:
                    # missing heartbeat — alert
                    write_alert(device_id, info["ts"], f"missing-heartbeat (last seen {int(delta)}s ago)", details=info["entry"])
                elif info["entry"].get("status") == "ERROR":
                    write_alert(device_id, info["ts"], "device-reported-error", details=info["entry"])
            time.sleep(args.scan_interval)
    except KeyboardInterrupt:
        print("\nMonitor stopped by user.")
