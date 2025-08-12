# Day 8 — Cloud Monitoring: RCA Template

## Incident summary
- **Incident ID:** D8-001
- **Detected on:** 2025-08-12T08:15:42Z (UTC)
- **Device ID(s):** dev-1
- **Symptom:** Device self-reported ERROR with reason "low-battery"

## Impact
- Who/what was affected -  Device dev-1

## Timeline
- **2025-08-12T08:15:40Z** — Last heartbeat received from dev-1 with status: ERROR, reason: low-battery.
- **2025-08-12T08:15:42Z** — Monitor detected the error and logged an alert.

## Diagnostic steps performed
- Reviewed heartbeat log (`device_heartbeats.log`) and confirmed error event.
- Checked monitor output (`alerts.json` and `alerts.log`) for device dev-1.
- Verified that device dev-1 sent a valid heartbeat but status=ERROR indicated low-battery.

## Root cause hypothesis
- Simulated device battery level dropped below operational threshold, triggering an internal ERROR status.

## Resolution / Mitigation
- Replace/recharge device battery.
- Implement proactive alerts when battery < 30% to prevent downtime.

## Notes / Evidence
**Alert JSON:**
```json
[
  {
    "alert_ts": "2025-08-12T08:15:42Z",
    "device_id": "dev-1",
    "reason": "device-reported-error",
    "detected_at": "2025-08-12T08:15:40Z",
    "details": {
      "ts": "2025-08-12T08:15:40Z",
      "device_id": "dev-1",
      "status": "ERROR",
      "reason": "low-battery"
    }
  }
]
