#!/usr/bin/env python3
"""
Device Heartbeat Simulator — HIPAA/GDPR-safe
- Writes sanitized heartbeat/error events to device_heartbeats.log
- Sends NON-PII metrics to CloudWatch (if boto3 & creds present)
- Demo PII fields can be added with --demo-pii but will be masked in logs

Usage examples:
  python cloud-monitoring/device_simulator.py
  python cloud-monitoring/device_simulator.py --devices 5 --interval 3 --drop-rate 0.2 --demo-pii
"""

import time
import json
import random
import argparse
from datetime import datetime, UTC

LOG_FILE = "device_heartbeats.log"

# ---- Optional CloudWatch (won't fail if boto3 not installed) ----
CW_ENABLED = False
try:
    import boto3
    cloudwatch = boto3.client("cloudwatch")
    CW_ENABLED = True
except Exception:
    cloudwatch = None
    CW_ENABLED = False


# -------------------- Compliance Helpers --------------------
def sanitize_log_entry(entry: dict) -> dict:
    """
    Remove or mask sensitive info to meet HIPAA/GDPR requirements.
    Masks common PII/PHI fields if present; safe to call on any entry.
    """
    sanitized = entry.copy()

    # Names
    for k in ("patient_name", "full_name", "name"):
        if k in sanitized and sanitized[k]:
            sanitized[k] = "REDACTED"

    # Identifiers (MRN, patient_id, SSN, phone, email)
    if "patient_id" in sanitized and sanitized["patient_id"]:
        pid = str(sanitized["patient_id"])
        sanitized["patient_id"] = f"{pid[:3]}****" if len(pid) >= 3 else "****"

    if "mrn" in sanitized and sanitized["mrn"]:
        mrn = str(sanitized["mrn"])
        sanitized["mrn"] = f"{mrn[:3]}****"

    if "ssn" in sanitized and sanitized["ssn"]:
        sanitized["ssn"] = "***-**-****"

    if "phone" in sanitized and sanitized["phone"]:
        sanitized["phone"] = "REDACTED"

    if "email" in sanitized and sanitized["email"]:
        sanitized["email"] = "redacted@example.com"

    # Addresses / DOB
    for k in ("address", "dob", "date_of_birth"):
        if k in sanitized and sanitized[k]:
            sanitized[k] = "REDACTED"

    return sanitized


def iso_now() -> str:
    # timezone-aware UTC, safe for logs & metrics
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def put_metric_safe(metric_name: str, value: float, device_id: str, extra_dim: dict | None = None):
    """
    Send NON-PII metrics to CloudWatch. Ignores if CloudWatch is unavailable.
    Dimensions are restricted to non-identifying technical fields.
    """
    if not CW_ENABLED:
        return
    dims = [{"Name": "DeviceID", "Value": device_id}]
    if extra_dim:
        for k, v in extra_dim.items():
            # Only allow non-PII dimensions
            if k.lower() in {"errortype", "status"}:
                dims.append({"Name": k, "Value": str(v)})

    try:
        cloudwatch.put_metric_data(
            Namespace="IoTDeviceMetrics",
            MetricData=[{
                "MetricName": metric_name,
                "Dimensions": dims,
                "Timestamp": datetime.now(UTC),
                "Value": float(value),
                "Unit": "Count" if metric_name == "ErrorCount" else "None",
            }]
        )
    except Exception:
        # Keep simulator resilient; never crash on metrics
        pass


# -------------------- Simulator Core --------------------
def simulate(devices, interval, drop_rate, demo_pii=False):
    """
    devices: list of device IDs (ints)
    interval: seconds between heartbeats per device
    drop_rate: probability (0..1) to skip or error a heartbeat
    demo_pii: include fake PII fields (will be masked in logs)
    """
    print(f"Starting simulator: devices={len(devices)} interval={interval}s drop_rate={drop_rate} demo_pii={demo_pii}")
    try:
        while True:
            for d in devices:
                entry = None
                # randomly skip heartbeat or emit an error
                if random.random() < drop_rate:
                    if random.random() < 0.5:
                        # explicit error entry
                        err_type = random.choice(["sensor-fault", "low-battery", "comm-failure"])
                        entry = {
                            "ts": iso_now(),
                            "device_id": f"dev-{d}",
                            "status": "ERROR",
                            "reason": err_type
                        }
                        put_metric_safe("ErrorCount", 1, device_id=f"dev-{d}", extra_dim={"ErrorType": err_type})
                    else:
                        # silent drop (no entry written)
                        entry = None
                else:
                    # OK heartbeat
                    entry = {
                        "ts": iso_now(),
                        "device_id": f"dev-{d}",
                        "status": "OK",
                        "battery": random.randint(30, 100),
                        "metric": round(random.uniform(0.0, 200.0), 2),
                    }
                    # Send non-PII metrics
                    put_metric_safe("BatteryLevel", entry["battery"], device_id=f"dev-{d}")
                    put_metric_safe("MetricReading", entry["metric"], device_id=f"dev-{d}")

                # (Optional) add fake PII to prove masking works
                if entry and demo_pii:
                    entry.update({
                        "patient_name": random.choice(["John Doe", "Jane Smith", "Alice Johnson"]),
                        "patient_id": str(random.randint(100000, 999999)),
                        "dob": "1980-01-01",
                        "phone": "(555) 555-1212",
                        "email": "john.doe@example.com",
                        "address": "123 Main St, Hometown, NY"
                    })

                if entry:
                    # Sanitize before writing anywhere
                    sanitized = sanitize_log_entry(entry)
                    line = json.dumps(sanitized)
                    with open(LOG_FILE, "a", encoding="utf-8") as fh:
                        fh.write(line + "\n")
                    print(f"[sim] wrote (sanitized): {line}")

                # small sleep between device heartbeats so timestamps vary
                time.sleep(interval / max(1, len(devices)))
            # brief pause after each cycle through all devices
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\nSimulator stopped by user.")


# -------------------- CLI --------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HIPAA/GDPR-safe device heartbeat simulator")
    parser.add_argument("--devices", type=int, default=3, help="Number of simulated devices")
    parser.add_argument("--interval", type=float, default=5.0, help="Heartbeat interval (seconds)")
    parser.add_argument("--drop-rate", type=float, default=0.0, help="Probability to drop/error heartbeat (0..1)")
    parser.add_argument("--demo-pii", action="store_true", help="Include fake PII fields to demonstrate masking")
    args = parser.parse_args()

    devices = list(range(1, args.devices + 1))
    simulate(devices, args.interval, args.drop_rate, demo_pii=args.demo_pii)

