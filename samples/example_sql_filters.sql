-- Example SQL filters and queries for log analysis
-- These examples illustrate time filtering, WHERE clauses, aggregation, and simple sanitization.

-- 1) Basic time-range filter (Postgres / MySQL compatible timestamp column)
-- Select events in the last 7 days
SELECT *
FROM logs
WHERE event_time >= now() - interval '7 days';

-- 2) Filter by severity and source IP
SELECT source_ip, COUNT(*) AS hits
FROM logs
WHERE severity IN ('ERROR','CRITICAL')
  AND source_ip IS NOT NULL
  AND event_time >= now() - interval '30 days'
GROUP BY source_ip
ORDER BY hits DESC
LIMIT 50;

-- 3) Using parameterized queries (avoid SQL injection) - example for prepared statements
-- In application code, pass params instead of formatting strings.
-- Example (psuedocode): db.execute("SELECT * FROM logs WHERE user_id = %s", [user_id])

-- 4) Aggregation and pivot: top sources per severity
SELECT severity, source_ip, COUNT(*) AS cnt
FROM logs
WHERE event_time >= now() - interval '1 day'
GROUP BY severity, source_ip
ORDER BY severity, cnt DESC
LIMIT 100;

-- 5) Window function: detect spikes per source
SELECT source_ip, event_time,
  COUNT(*) OVER (PARTITION BY source_ip ORDER BY event_time RANGE BETWEEN INTERVAL '1 hour' PRECEDING AND CURRENT ROW) AS events_last_hour
FROM logs
WHERE event_time >= now() - interval '1 day';

-- 6) Suggestions: ensure indexes on event_time and source_ip for performance
-- CREATE INDEX idx_logs_event_time ON logs(event_time);
-- CREATE INDEX idx_logs_source_ip ON logs(source_ip);
