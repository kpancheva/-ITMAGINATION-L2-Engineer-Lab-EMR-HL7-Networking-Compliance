-- Create patients table
CREATE TABLE IF NOT EXISTS patients (
    patient_id INT PRIMARY KEY,
    name VARCHAR(100)
);

-- Create alerts table
CREATE TABLE IF NOT EXISTS alerts (
    alert_id SERIAL PRIMARY KEY,
    alert_type VARCHAR(100),
    patient_id INT REFERENCES patients(patient_id),
    timestamp TIMESTAMP
);

-- Insert sample patients
INSERT INTO patients (patient_id, name) VALUES
(101, 'John Doe'),
(102, 'Jane Smith'),
(103, 'Alice Johnson');

-- Insert sample alerts
INSERT INTO alerts (alert_type, patient_id, timestamp) VALUES
('HL7 parse failure', 101, '2025-08-11 09:13:02'),
('HL7 parse failure', 102, '2025-08-11 10:15:20'),
('Device down', 103, '2025-08-11 11:00:00');
