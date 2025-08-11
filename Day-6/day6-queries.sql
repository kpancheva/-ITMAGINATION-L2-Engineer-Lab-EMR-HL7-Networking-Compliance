SELECT * FROM alerts WHERE alert_type = 'HL7 parse failure' ORDER BY timestamp DESC LIMIT 10;

SELECT p.patient_id, p.name, COUNT(a.alert_id) AS alert_count  
FROM patients p  
JOIN alerts a ON p.patient_id = a.patient_id  
GROUP BY p.patient_id, p.name  
ORDER BY alert_count DESC;
