#!/usr/bin/env python3
"""HL7 Alert Handler for Dialysis Machine Support"""

import logging
from datetime import datetime

class HL7AlertHandler:
    def __init__(self):
        self.alert_count = 0
        logging.info("HL7 Alert Handler initialized")

    def analyze_hl7(self, message):
        """Analyze HL7 messages from dialysis machines"""
        alerts = []
        
        # 1. Check for missing/invalid MSH segment
        if not message.startswith("MSH|^~\\&"):
            alerts.append(self._build_alert(
                alert_type="HL7_PROTOCOL_ERROR",
                severity="CRITICAL",
                rca="Missing or corrupt MSH segment - message not HL7-compliant",
                action="1. Check dialysis machine HL7 settings\n2. Verify physical connection"
            ))
        
        # 2. Check for missing treatment data
        elif "ORU^R01" in message and "OBX|" not in message:
            alerts.append(self._build_alert(
                alert_type="DATA_MISSING",
                severity="HIGH",
                rca="No treatment data (OBX segments) found in ORU message",
                action="1. Restart data export module\n2. Check patient monitor connections"
            ))
        
        # 3. Check for abnormal dialysis metrics
        abnormal = self._check_abnormal_values(message)
        if abnormal:
            alerts.append(abnormal)
        
        return alerts

    def _build_alert(self, alert_type, severity, rca, action):
        """Standardize alert format"""
        self.alert_count += 1
        return {
            "alert_id": f"ALERT-{datetime.now().strftime('%Y%m%d')}-{self.alert_count}",
            "type": alert_type,
            "severity": severity,
            "timestamp": datetime.now().isoformat(),
            "rca": rca,
            "action": action
        }

    def _check_abnormal_values(self, message):
        """Check for clinically dangerous values"""
        try:
            if "KtV^Dialysis Adequacy" in message:
                ktv = float(message.split("KtV^Dialysis Adequacy||")[1].split("|")[0])
                if ktv < 1.2:
                    return self._build_alert(
                        alert_type="LOW_KTV",
                        severity="HIGH",
                        rca=f"Insufficient dialysis dose (Kt/V={ktv:.2f} < 1.2)",
                        action="1. Review treatment parameters\n2. Check vascular access"
                    )
        except (IndexError, ValueError) as e:
            logging.warning(f"Value parsing error: {str(e)}")
        return None

    def generate_support_ticket(self, alert):
        """Format for L2 support workflow"""
        return f"""
[DIALYSIS HL7 ALERT - {alert['alert_id']}]
Severity: {alert['severity']}
Type: {alert['type']}
Timestamp: {alert['timestamp']}

ROOT CAUSE:
{alert['rca']}

REQUIRED ACTIONS:
{alert['action']}

ESCALATION PATH:
- L1: Verify device connectivity
- L2: Review HL7 config (Ref: KB-HL7-{alert['type']})
- L3: Engage clinical engineering
------------------------------
"""

# Test function
def test_alert_handler():
    """Run sample tests if executed directly"""
    handler = HL7AlertHandler()
    test_msgs = [
        "MSH|^~\\&|Dialysis|||202402061200||ORU^R01|123|P|2.3\nPID|||1",  # Missing OBX
        "BAD_HEADER|...",  # Invalid MSH
        rf"""MSH|^~\&|Dialysis|||202402061200||ORU^R01|123|P|2.3
PID|||1
OBR|1|||1234^Dialysis
OBX|1|NM|KtV^Dialysis Adequacy||1.0||1.2-2.0||||F"""  # Low Kt/V
    ]
    
    for msg in test_msgs:
        print(f"\nTesting message:\n{msg}")
        alerts = handler.analyze_hl7(msg)
        for alert in alerts:
            print(handler.generate_support_ticket(alert))

if __name__ == "__main__":
    test_alert_handler()