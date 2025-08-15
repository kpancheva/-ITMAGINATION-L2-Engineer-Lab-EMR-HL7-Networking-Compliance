## Common Dialysis Machine HL7 Errors

1. **Missing MSH Segment**  
   - Symptom: Messages rejected by EMR  
   - RCA: Device HL7 export misconfiguration  
   - Fix: Verify protocol settings on dialysis machine  

2. **Empty OBX Segments**  
   - Symptom: Treatments not recorded  
   - RCA: Data export interrupted during treatment  
   - Fix: Restart data module → Check patient monitor connections  

3. **Invalid Checksum**  
   - Symptom: Messages fail validation  
   - RCA: Network corruption or device firmware bug  
   - Fix: Test with cable replacement → Escalate to L3 if persistent  