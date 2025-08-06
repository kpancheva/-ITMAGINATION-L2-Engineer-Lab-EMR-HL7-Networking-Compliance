# Connectivity Tests and Network Commands

---

## 1. Ping Command

**Purpose:**  
Checks if a host is reachable and measures round-trip time for messages sent from the originating host to a destination computer.

**Command:**

```bash
ping 127.0.0.1


Result:
Pinging 127.0.0.1 with 32 bytes of data:
Reply from 127.0.0.1: bytes=32 time<1ms TTL=128
Reply from 127.0.0.1: bytes=32 time<1ms TTL=128
Reply from 127.0.0.1: bytes=32 time<1ms TTL=128
Reply from 127.0.0.1: bytes=32 time<1ms TTL=128

Ping statistics for 127.0.0.1:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 0ms, Maximum = 0ms, Average = 0ms


## Traceroute (tracert) Test to 127.0.0.1

Command:

tracert 127.0.0.1

Purpose:
To trace the path packets take from your machine to the destination IP address.


Result: 
Tracing route to 127.0.0.1 over a maximum of 30 hops:

  1    <1 ms    <1 ms    <1 ms  localhost [127.0.0.1]

Trace complete.

Interpretation:
Since 127.0.0.1 is the loopback address, the traceroute completes in a single hop, showing the packet never left the machine. This confirms local network stack functionality.

Use Case:
Useful for checking the path and latency to remote devices or servers on the network.


## 3. Netstat Command

**Purpose:**  
Displays all active network connections, listening ports, and their current states.

**Command:**

```bash
netstat -an


Result:
Active Connections

  Proto  Local Address          Foreign Address        State
  TCP    0.0.0.0:80             0.0.0.0:0              LISTENING
  TCP    0.0.0.0:135            0.0.0.0:0              LISTENING
  TCP    0.0.0.0:445            0.0.0.0:0              LISTENING


Use Case:
To verify if a service (e.g. Mirth HL7 listener on port 2575) is up and accepting connections.