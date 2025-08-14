import json

def handle_device_message(message: str):
    if not message.strip():  # skip empty lines
        return
    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        print(f"[WARN] Skipping invalid JSON line: {message}")
        return

    if data.get("status") == "ERROR":
        device_id = data.get("device_id")
        reason = data.get("reason", "unknown")
        print(f"[ALERT] Device {device_id} reported an ERROR: {reason}")
    else:
        print(f"[INFO] Device {data.get('device_id')} OK")

if __name__ == "__main__":
    log_file = "device_heartbeats.log"
    with open(log_file, "r") as f:
        for line in f:
            handle_device_message(line.strip())

