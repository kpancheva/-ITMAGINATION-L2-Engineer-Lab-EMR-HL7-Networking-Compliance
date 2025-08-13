# Day 11 – HIPAA & GDPR Compliance Simulation

## 1. Overview
This document simulates security and compliance measures for handling Protected Health Information (PHI) under HIPAA and Personally Identifiable Information (PII) under GDPR in the context of our HL7 IoT device integration project.

---

## 2. Applicable Regulations

| Regulation | Scope | Key Requirements |
|------------|-------|------------------|
| **HIPAA**  | U.S. healthcare sector – PHI | Privacy Rule, Security Rule, Audit Trails, Minimum Necessary, De-identification |
| **GDPR**   | EU – PII of EU citizens | Consent, Right to Access, Right to Erasure, Data Minimization, Breach Notification within 72 hrs |

---

## 3. Data Handling Policy
1. **Collection** – Only minimal required PHI/PII is collected from devices and HL7 messages.
2. **Transmission** – All data in transit is encrypted using TLS 1.2+.
3. **Storage** – Data at rest is encrypted using AES-256.
4. **Access Control** – Role-based access enforced. Only authorized personnel can access PHI/PII.
5. **Logging** – All access and message transactions logged with timestamps for audit purposes.
6. **Retention** – Logs containing PHI/PII are retained only for the legally required period and then securely deleted.

---

## 4. Audit Logging Example

### Python Implementation
```python
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename="audit.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def log_access(user, action, record_id):
    logging.info(f"User={user} | Action={action} | RecordID={record_id}")

# Example usage
log_access("nurse_a", "VIEW", "HL7MSG-12345")
