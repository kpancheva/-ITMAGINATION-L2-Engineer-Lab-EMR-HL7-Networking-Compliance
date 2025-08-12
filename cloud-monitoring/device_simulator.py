#!/usr/bin/env python3
"""
device_simulator.py
Simulate multiple cloud-connected medical devices sending periodic heartbeats
to a local log file: device_heartbeats.log

Usage:
  python device_simulator.py --devices 3 --interval 5 --drop-rate 0.1
"""

import time
import json
import random
import argparse
from datetime import datetime

LOG_FILE = "device_heartbeats.log"

def iso_now():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def simulate(devices, interval, drop_rate):
    """
    devices: list of device IDs (ints)
    interval: seconds between heartbeats per device
    drop_rate: probability (0..1) that a heartbeat will be skipped (simulate network/device failure)
    """
    print(f"Starting simulator: devices={len(devices)} interval={interval}s drop_rate={drop_rate}")
    try:
        while True:
            for d in devices:
                # randomly skip heartbeat to simulate packet loss / device issue
                if random.random() < drop_rate:
                    # skip writing this heartbeat
                    if random.random() < 0.3:
                        # occasionally produce an explicit error entry
                        entry = {
                            "ts": iso_now(),
                            "device_id": f"dev-{d}",
                            "status": "ERROR",
                            "reason": random.choice(["sensor-fault", "low-battery", "comm-failure"])
                        }
                    else:
                        # silent skip (no heartbeat written)
                        entry = None
                else:
                    entry = {
                        "ts": iso_now(),
                        "device_id": f"dev-{d}",
                        "status": "OK",
                        "battery": random.randint(30, 100),
                        "metric": round(random.uniform(0.0, 200.0), 2)
                    }

                if entry:
                    line = json.dumps(entry)
                    with open(LOG_FILE, "a", encoding="utf-8") as fh:
                        fh.write(line + "\n")
                    print(f"[sim] wrote: {line}")

                # small sleep between device heartbeats so timestamps vary
                time.sleep(interval / max(1, len(devices)))
            # after one round of all devices, sleep a bit (simulates real behavior)
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\nSimulator stopped by user.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--devices", type=int, default=3, help="Number of simulated devices")
    parser.add_argument("--interval", type=float, default=5.0, help="Heartbeat interval (seconds)")
    parser.add_argument("--drop-rate", type=float, default=0.0, help="Probability to drop heartbeat (0..1)")
    args = parser.parse_args()

    devices = list(range(1, args.devices + 1))
    simulate(devices, args.interval, args.drop_rate)
