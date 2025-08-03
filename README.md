# -ITMAGINATION-L2-Engineer-Lab-EMR-HL7-Networking-Compliance
This repository contains hands-on simulations and tools for preparing for an L2 Application Support role with a focus on healthcare systems, particularly EMR integrations (EPIC, HL7), network troubleshooting, compliance (HIPAA/GDPR), and SQL diagnostics.

 🩺 Purpose

To simulate real-world healthcare IT support scenarios, including:

- Device-to-EMR HL7 message flow
- Network connectivity & VLAN issues
- SQL-based diagnostics & RCA
- HIPAA/GDPR-aligned compliance configuration

## 🔧 Tools & Technologies

- **Mirth Connect** (HL7 Interface Engine)
- **PostgreSQL**
- **Python** (HL7 sender)
- **Wireshark**, **pfSense**, **Cisco Packet Tracer**
- **Docker**, **Azure/AWS Basics**
- **Markdown for RCA documentation**

## 📁 Structure

| Folder | Description |
|--------|-------------|
| `hl7-integration/` | Simulate HL7 message flow using Mirth Connect |
| `networking-lab/` | VLAN, DNS, firewall config and troubleshooting |
| `cloud-monitoring/` | Simulate device heartbeat and monitoring |
| `sql-diagnostics/` | Analyze medical data and troubleshoot delays |
| `security-compliance/` | HIPAA/GDPR simulation, audit logging |
| `rca-scenarios/` | Root Cause Analysis templates and writeups |
| `diagrams/` | Architecture and network flow diagrams |

## 📦 Quick Start (HL7 Lab)

1. Install [Mirth Connect](https://www.nextgen.com/products-and-services/integration-engine)
2. Import the channel from `hl7-integration/mirth-channel-export.xml`
3. Run `send_hl7.py` to send test messages
4. View output in PostgreSQL (`hl7-integration/postgres-schema.sql`)
5. Use Wireshark to monitor TCP port 2575 traffic

## 📋 Licensing

MIT License — use, fork, and modify freely.
