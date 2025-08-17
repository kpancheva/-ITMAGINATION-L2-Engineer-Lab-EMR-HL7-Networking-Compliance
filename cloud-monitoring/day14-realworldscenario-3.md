# **Day 14: Real World Scenario 3 - Database Blocking Chain**  

## 🚨 Incident Overview
```text
INCIDENT ID:   DB-OUTAGE-20240817
ENVIRONMENT:  EPIC Clarity PRD (SQL Server 2019)
IMPACT:       Patient Census Dashboard Unavailable
DURATION:     2h 14m (14:30-16:44 UTC)
ROOT CAUSE:   Missing index + long-running MERGE statement

🔍 Step-by-Step Diagnosis
1. Blocking Chain Analysis (Emergency)
sql
-- Identify the head blocker and victims
SELECT 
    blocking.session_id AS blocking_spid,
    blocked.session_id AS victim_spid,
    blocked.wait_time/1000 AS wait_sec,
    blocked.wait_type,
    DB_NAME(blocked.resource_database_id) AS database_name,
    blocking.sql_text AS blocking_query
FROM (
    SELECT 
        r.session_id,
        r.blocking_session_id,
        r.wait_time,
        r.wait_type,
        r.resource_database_id,
        t.text AS sql_text
    FROM sys.dm_exec_requests r
    CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t
    WHERE r.blocking_session_id = 0
) blocking
JOIN (
    SELECT 
        r.session_id,
        r.blocking_session_id,
        r.wait_time,
        r.wait_type,
        r.resource_database_id
    FROM sys.dm_exec_requests r
    WHERE r.blocking_session_id <> 0
) blocked ON blocking.session_id = blocked.blocking_session_id;
Critical Finding:

text
BLOCKING_SPID | VICTIM_SPID | WAIT_SEC | WAIT_TYPE    | DATABASE    | QUERY_SNIPPET
--------------|------------|----------|--------------|-------------|------------------
1126          | 884         | 327      | LCK_M_S      | EPIC_Clarity| MERGE patient_visits...

2. Execution Plan Hotspot
diff
- |-- Clustered Index Scan (OBJECT:([patient_visits].[PK_patient_visits]), Cost: 89%)
+ |-- Index Seek (OBJECT:([IX_patient_visits_encounter_date]), Cost: 12%

3. Missing Index Recommendation
sql
CREATE NONCLUSTERED INDEX IX_patient_visits_encounter_date
ON patient_visits (patient_id, encounter_date)
INCLUDE (discharge_status, attending_provider_id)
WITH (ONLINE = ON, MAXDOP = 4);

🛠️ Corrective Actions
Immediate Mitigation:

sql
-- Kill the blocking session with rollback
KILL 1126 WITH STATUSONLY;
Permanent Fix:

Created covering index (reduced I/O by 87%)

Rewrote MERGE as batched INSERT/UPDATE

Added NOLOCK hints to reporting queries

📊 Performance Impact
Metric	Pre-Fix	Post-Fix
Dashboard Load Time	47s	1.9s
Blocking Incidents	12/hr	0/hr
CPU Usage	92%	34%
