import socket

# Sample HL7 ORU^R01 message
HL7_MESSAGE = """MSH|^~\\&|Device1|Ward1|EMR|Main|202508031010||ORU^R01|MSG00001|P|2.3
PID|||123456||DOE^JOHN
OBR|1|||DIA001^DIALYSIS^L
OBX|1|NM|BP^Blood Pressure||145|mmHg"""

def send_hl7(ip='127.0.0.1', port=2575):
    mllp = b'\x0b' + HL7_MESSAGE.encode('utf-8') + b'\x1c\x0d'  # MLLP framing
    with socket.create_connection((ip, port)) as sock:
        sock.sendall(mllp)
        print(f"HL7 message sent successfully to {ip}:{port}")


if __name__ == "__main__":
    send_hl7()
