L2 Application Support Engineer (Healthcare IT Focus)

This repository contains hands-on simulations and tools for preparing for an L2 Application Support role with a focus on healthcare systems, particularly EMR integrations (EPIC, HL7), network troubleshooting, compliance (HIPAA/GDPR), and SQL diagnostics.

 🩺 Purpose

To simulate real-world healthcare IT support scenarios, including:

- Device-to-EMR HL7 message flow
- Network connectivity & VLAN issues
- SQL-based diagnostics & RCA
- Simulation of cloud-connected medical device monitoring with alerting
- HIPAA/GDPR-aligned compliance configuration

🔧 Tools & Technologies Used

    Mirth Connect - HL7 Interface Engine for message routing and transformation

    PostgreSQL - Database for storing and querying HL7 data and alerts

    Python - Automation and HL7 message sending/parsing scripts

    Wireshark - Network packet capture for troubleshooting

    pfSense, Cisco Packet Tracer - Network devices and VLAN/firewall simulation

    Docker & Azure/AWS Basics - For containerization and cloud connectivity concepts

    Markdown - For writing detailed RCA and incident reports

📁 Repository Structure
Folder	Description
hl7-integration/	Simulate HL7 message flow using Mirth Connect
networking-lab/	VLAN, DNS, firewall configuration and troubleshooting
cloud-monitoring/	Simulate cloud-connected medical device heartbeats, generate alerts, and perform downtime RCA
sql-diagnostics/	Analyze healthcare data with SQL queries and perform diagnostics and RCA
security-compliance/	HIPAA & GDPR security simulations, audit logging, and policy configuration
rca-scenarios/	Root Cause Analysis templates, incident writeups, and best practice documentation
diagrams/	Architecture diagrams, network flowcharts, and visual aids

## 📦 Quick Start (HL7 Lab)

1. Install [Mirth Connect](https://www.nextgen.com/products-and-services/integration-engine)
2. Import the channel from `hl7-integration/mirth-channel-export.xml`
3. Run `send_hl7.py` to send test messages
4. View output in PostgreSQL (`hl7-integration/postgres-schema.sql`)
5. Use Wireshark to monitor TCP port 2575 traffic

## 📋 Licensing

MIT License 
