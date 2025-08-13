# Day 11 – HIPAA/GDPR-Safe Device Simulator & Cloud Monitoring

**Date:** 2025-08-13  
**Project:** Cloud IoT Device Monitoring

---

## Objective

Enhance the device simulator to:

1. Generate heartbeat and error events for multiple IoT devices.
2. Demonstrate safe handling of sensitive data (PII/PHI) for HIPAA/GDPR compliance.
3. Send **non-PII metrics** to AWS CloudWatch for automated monitoring.

---

## Key Updates to Simulator

- Added **`sanitize_log_entry`** function to mask/remove sensitive fields:
  - Names, patient IDs, SSNs, phone numbers, email addresses, DOB, addresses.
  - Fake PII can be included with `--demo-pii` but is **always sanitized** before logging or metrics.
- Non-PII metrics sent to CloudWatch:
  - `BatteryLevel`
  - `MetricReading`
  - `ErrorCount` (with only `DeviceID` and `ErrorType` as dimensions)
- CloudWatch metrics are **technical**, no sensitive info is exposed.
- Supports multiple devices with configurable heartbeat interval and error/drop probability.

---

## Example Usage

```bash
# Run simulator with 3 devices, 5-second heartbeat, 30% error/drop rate, fake PII demo
python device_simulator.py --devices 3 --interval 5 --drop-rate 0.3 --demo-pii
