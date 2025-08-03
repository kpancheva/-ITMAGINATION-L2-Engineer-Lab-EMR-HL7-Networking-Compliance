import socket
import hl7

def start_listener():
    host = '127.0.0.1'
    port = 2575

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"HL7 listener started on {host}:{port}... Waiting for messages.")
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connection from {addr}")
                data = conn.recv(4096).decode('utf-8')
                if not data:
                    continue

                # Parse HL7 message
                message = hl7.parse(data)
                print("Parsed HL7 message:")

                # Extract and print key segments
                for segment in message:
                    if segment[0] == 'MSH':
                        print(f"MSH - Sending Application: {segment[2]}, Receiving Application: {segment[4]}")
                    elif segment[0] == 'PID':
                        print(f"PID - Patient ID: {segment[3]}, Patient Name: {segment[5]}")
                    elif segment[0] == 'OBX':
                        print(f"OBX - Observation ID: {segment[3]}, Value: {segment[5]}")

                print("Full raw HL7 message:")
                print(data)
                print("\n--- End of Message ---\n")
                
                
                # Save raw message to logs
                with open("logs/received_message.hl7", "a") as f:
                    f.write(data + "\n\n")


if __name__ == "__main__":
    start_listener()
