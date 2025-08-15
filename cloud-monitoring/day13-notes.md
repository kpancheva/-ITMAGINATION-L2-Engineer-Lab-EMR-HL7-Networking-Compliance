# Day 13: Dialysis HL7 Alert Monitoring System

## Objectives Achieved
- ✅ Built an end-to-end HL7 monitoring pipeline for dialysis machines  
- ✅ Implemented L2-support-focused alerting with:  
  - Root Cause Analysis (RCA)  
  - Actionable steps  
  - Escalation paths  
- ✅ Solved real-world Python issues (escape sequences, imports)  

## Files Created
| File | Purpose | Key Features |
|------|---------|--------------|
| `dialysis_hl7_simulator.py` | Simulates dialysis machines | CLI arguments, HL7 message generation |  
| `alert_handler.py` | Analyzes HL7 messages | LOW_KTV detection, support tickets |  
| `demo_errors.hl7` | Test cases | Predefined error scenarios |  

## Lessons Learned
1. **HL7 Protocol**: Used raw strings (`r""`) for delimiter sequences.  
2. **Error Handling**: Added file validation and graceful fallbacks.  
3. **Support Workflows**: Structured alerts to mirror real clinical escalation.  
