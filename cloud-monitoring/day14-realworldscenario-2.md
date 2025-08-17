# Day 14: Dual Failure Scenario - Network & Database Issues

## 🌐 Scenario 1: Network Connectivity Failure.

### 🚨 Incident Summary
| Key Information       | Details                                  |
|-----------------------|------------------------------------------|
| **Error**            | `HL7 Connection Timeout`                |
| **Impact**           | EPIC ADT Interfaces Down                |
| **Duration**         | 38 minutes                              |

### 🔍 Troubleshooting Steps

First, I would feviry the physical connectivity with a ping command to the IP, e.g

ping 10.20.30.1 -n 5 -w 1000

-n 5: Specifies the number of echo requests (pings) to send. In this case, it will send 5 pings before stopping.

-w 1000: Sets the timeout (in milliseconds) to wait for each reply. Here, it will wait 1000 ms (1 second) for each reply before considering it a timeout. 

This command will ping 10.20.30.1 five times and wait up to 1 second for each reply.

If there is a packet loss, check the switch port next.
If ping is 100% successful, I'd proceed to Step 2 (Test Application Port)

For switch port check (if ping fails):
This requires coordination with the network team and this command should be shared with them: 

show interface GigabitEthernet0/1 | include connected|error

Logic Flow:
Ping Results:
├── Success (0% loss) → Proceed to Step 2
└── Failure (any loss) → Attempt switch check → Document findings → Proceed to Step 2 anyway

If ping is 100% successful, you can proceed to Step 2 (Test Application Port)

🔧 Step 2: Test Application Port (HL7/EPIC Connectivity)

Verify if the application port (TCP/5000) is reachable through the network path, regardless of physical layer issues.

If using Linux I'd run the following command:

telnet epic-hl7.example.com 5000

Interpret Results:
- TcpTestSucceeded: True	 - The port is open and reachable, proceed to Step 3
- Connection timed out	- Firewall/ACL blocking traffic. Document and escalate to network team
- No route to host	- Network unreachable (physical issue). I'd go back to step 1
- Connection refused - Service not listening on port. Escalate to application team

🔧 Step 3: Trace Network Path (Route Analysis)
-  Identify where packets are being dropped or delayed between the machine and the HL7 endpoint (epic-hl7.example.com:5000).

In bash run te following command:
mtr --report --report-cycles 5 epic-hl7.example.com 

Command Breakdown:
mtr

A network diagnostic tool that combines the functionality of traceroute and ping.

It continuously probes a network path to measure latency and packet loss.

--report

Runs mtr in report mode, meaning it will run for a set number of cycles and then print statistics before exiting.

Unlike the interactive mode (default), this mode is useful for scripting and automated testing.

--report-cycles 5

Specifies the number of pings (cycles) to send to each hop before generating the report.

Here, 5 means each hop will be tested 5 times before displaying results.

epic-hl7.example.com

The destination hostname or IP address being tested.

What This Command Does?:
Sends 5 pings to each hop along the route to epic-hl7.example.com.

After completing the cycles, it prints a summary report showing:

- Each hop (router) along the path.

- Packet loss percentage.

- Latency statistics (avg, min, max).

- Network performance issues (if any).

Example output:
Start: 2025-08-17T12:00:00+0000
HOST: your-pc.example.com          Loss%   Snt   Last   Avg  Best  Wrst StDev
  1.|-- router.local                0.0%     5    2.1   2.3   2.0   2.6   0.2
  2.|-- isp-gateway.example.net     0.0%     5   10.2  10.5   9.8  11.2   0.5
  3.|-- data-center.example.com    20.0%     5   25.1  24.8  23.5  26.2   1.1
  4.|-- epic-hl7.example.com        0.0%     5   30.0  29.7  28.9  30.5   0.6
Hop 3 shows 20% packet loss, indicating a possible network issue.

If the loss only appears occasionally, it might be temporary congestion.

If it’s consistent (e.g., always 20% at the same hop), proceed to investigate.

Key Notes:
Not all packet loss is critical. If the final hop has 0% loss, the connection may still work fine.

ICMP throttling: Many networks deprioritize ping traffic, so losses may not affect actual data (e.g., HL7 messages over TCP).

Example Next Steps:
Rerun with TCP mode:

bash
mtr --tcp --report --report-cycles 10 epic-hl7.example.com

If the loss persists at the same hop, contact your ISP with the report.

If the loss is at the destination,I'd reach out to Epic HL7 support.


❌ Possible Gaps to Address:
1. Is the Packet Loss Actually Impacting HL7 Traffic?
Action: Test with a real HL7 message (e.g., send a test ADT^A01 via TCP).

Use tcpdump or Wireshark to check for retransmissions/drops:

bash
sudo tcpdump -i any host epic-hl7.example.com -w hl7_traffic.pcap
Why? ICMP loss might not correlate with TCP-based HL7 traffic.

2. Is the Problem Intermittent or Time-Based?
Action: Run mtr at different times (peak vs. off-peak hours).

Use a loop to log results:

bash
for i in {1..12}; do mtr --report --report-cycles 5 epic-hl7.example.com >> mtr_logs.txt; sleep 300; done


3. Is There a Routing Issue?
Action: Trace the route from another ASN (e.g., AWS/Azure VM) to check for asymmetric routing.

Compare paths:

bash
mtr --report --report-cycles 5 epic-hl7.example.com  # From your location  

mtr --report --report-cycles 5 epic-hl7.example.com  # From a cloud VM


4. Are Firewalls/ACLs Blocking Traffic?
Action: If the loss is at the destination, confirm:

- Epic HL7’s firewall allows your IP.

- No ACLs are dropping packets (e.g., rate-limiting).

- Tool: Ask Epic support to check server-side packet captures.

If all steps above are done and the issue persists, escalate to:

Your ISP (demand traceroute/ping tests from their backbone).

Epic HL7 Team (request MTR logs from their end back to you).

If the loss is confirmed but HL7 traffic works fine, document it as a non-critical anomaly (e.g., "ICMP throttling at Hop 3, no impact on HL7 throughput").