#!/usr/bin/env python3
import json
from pathlib import Path

log_path = Path("monitoring.log")
alerts = []

if not log_path.exists():
    print("monitoring.log not found. Create the file and re-run.")
    raise SystemExit(1)

with log_path.open() as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue
        # simple patterns for WARN and ERROR
        if "WARN" in line or "ERROR" in line:
            # parse simple timestamp / level / message
            # format: [YYYY-MM-DD HH:MM:SS] LEVEL - message
            try:
                ts_end = line.index("]")
                timestamp = line[1:ts_end]
                remainder = line[ts_end+2:]
                level, msg = remainder.split(" - ", 1)
                level = level.strip()
            except Exception:
                timestamp = ""
                level = "UNKNOWN"
                msg = line

            alert = {
                "timestamp": timestamp,
                "level": level,
                "message": msg
            }
            alerts.append(alert)
            print(f"ALERT: {timestamp} {level} - {msg}")

# write structured alerts to alerts.json
alerts_path = Path("alerts.json")
with alerts_path.open("w") as out:
    json.dump({"alerts": alerts}, out, indent=2)

print(f"\nFound {len(alerts)} alert(s). Written to {alerts_path.resolve()}")
