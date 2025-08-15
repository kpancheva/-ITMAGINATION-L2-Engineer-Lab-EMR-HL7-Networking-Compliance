#!/usr/bin/env python3
"""Dialysis Machine HL7 Simulator with Enhanced Alerting"""

import random
import time
import logging
import argparse
from datetime import datetime
from alert_handler import HL7AlertHandler

# Initialize alert system
alert_handler = HL7AlertHandler()

def generate_hl7_oru(patient_id):
    """Generate HL7 messages for dialysis patients"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return rf"""MSH|^~\&|Dialysis|||{timestamp}||ORU^R01|{random.randint(1000,9999)}|P|2.3
PID|||{patient_id}||Doe^John||19600101|M
OBR|1|||1234^Dialysis Treatment
OBX|1|NM|KtV^Dialysis Adequacy||{random.uniform(1.0, 2.0):.2f}||1.2-2.0||||F
OBX|2|ST|BP^Blood Pressure||{random.randint(90,140)}/{random.randint(60,90)}||||||F"""

def read_hl7_file(file_path):
    """Read pre-recorded HL7 messages from file"""
    try:
        with open(file_path, 'r') as f:
            return [msg.strip() for msg in f.read().split('\n\n') if msg.strip()]
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return []

def simulate_from_file(file_path):
    """Process messages from file instead of generating"""
    messages = read_hl7_file(file_path)
    if not messages:
        return
    
    for msg in messages:
        print(f"\nProcessing message:\n{msg}")
        alerts = alert_handler.analyze_hl7(msg)
        for alert in alerts:
            print(alert_handler.generate_support_ticket(alert))
        time.sleep(2)

def simulate_dialysis_messages():
    """Main simulation loop with enhanced alerts"""
    while True:
        message = generate_hl7_oru(f"DIAL{random.randint(100,999)}")
        print(f"\nGenerated message:\n{message}")
        
        alerts = alert_handler.analyze_hl7(message)
        for alert in alerts:
            ticket = alert_handler.generate_support_ticket(alert)
            logging.error(ticket)
            print(ticket)
        
        time.sleep(5)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('dialysis_alerts.log'),
            logging.StreamHandler()
        ]
    )

    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', help='Path to HL7 file for testing')
    args = parser.parse_args()

    if args.input_file:
        simulate_from_file(args.input_file)
    else:
        simulate_dialysis_messages()