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

graph LR
  A[Ping Results] --> B{0% loss?}
  B -->|Yes| C[Proceed to Step 2]
  B -->|No| D[Check switch port]
  D --> C

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
text
HOST: your-pc  
1.|-- router.local         0.0% loss  2.1ms avg  
2.|-- isp-gateway          0.0% loss 10.5ms avg  
3.|-- data-center         20.0% loss 24.8ms avg  <-- ISSUE  
4.|-- epic-hl7            0.0% loss 29.7ms avg  

Key Notes:

Hop 3 shows 20% loss → Possible ISP issue

ICMP loss ≠ HL7 TCP impact → Validate with tcpdump:

bash
sudo tcpdump -i any host epic-hl7.example.com -w hl7.pcap


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


🔧 Fixes Implemented
Firewall Rule Added:

cisco
access-list INTERFACE_ACL permit tcp 10.20.30.0 0.0.0.255 host epic-hl7.example.com eq 5000
Hardware Fix: Replaced SFP on Gi0/1.

📊 Results
text
| Metric          | Before | After  |  
|-----------------|--------|--------|  
| HL7 Throughput  | 12/sec | 53/sec |  
| Ping Loss       | 32%    | 0%     |  
