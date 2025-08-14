# Day 12 - Cloud Monitoring & Local Device Simulation

## Objectives
- Simulate device messages locally using Docker.
- Handle device alerts with a local Python handler.
- Understand mapping of local simulation to cloud/containerized workflows.

---

## Steps Performed

### 1. Verify Local Project Structure
- Checked files in `cloud-monitoring/`:
```bash
ls
Dockerfile  cloud-monitoring.py  device_simulator.py  day8-rca-template.md ...
Noted missing requirements.txt (caused build issue).

2. Docker Build & Issues
Built Docker image for device simulator:

bash
docker build -t device-simulator .
Issue: Build failed because requirements.txt was missing.

Resolution: Created minimal requirements.txt (even empty works for simulation), rebuilt image successfully.

3. Run Device Simulator Container
Command:

bash
docker run --name device-sim-runner --rm device-simulator
Simulator output:

text
Starting simulator: devices=3 interval=5.0s drop_rate=0.2 demo_pii=False
[sim] wrote (sanitized): {"ts": "...", "device_id": "dev-1", "status": "OK", "battery": 66, "metric": 82.24}
[sim] wrote (sanitized): {"ts": "...", "device_id": "dev-3", "status": "ERROR", "reason": "sensor-fault"}
4. Run Local Alert Handler
Command:

bash
python cloud-monitoring/local_alert_handler.py
Handler output:

text
[INFO] Device dev-1 OK
[ALERT] Device dev-3 reported an ERROR: sensor-fault
5. Issues Encountered
Missing container logs / Docker container disappeared

docker logs and docker stop failed because the container was already removed (--rm flag used).

JSON decode errors when trying to read empty or missing input

Fixed by ensuring simulator is running and outputting valid JSON.

Incorrect file paths

Ran local_alert_handler.py from the correct directory:

bash
python cloud-monitoring/local_alert_handler.py
6. Lessons Learned
Local Docker simulation is sufficient to test alert handling without spinning up AWS resources.

Important to verify file paths and requirements before building Docker images.

Mapping local setup to cloud deployment:

Local	Cloud
Docker container device_simulator.py	IoT devices / containerized service
local_alert_handler.py	Lambda / cloud container reading from queue
stdout [ALERT] messages	Cloud logs, SNS notifications, dashboards

