-- backend/supabase_cron.sql
-- Setup for pg_cron in Supabase

-- Example: Run a nightly job to aggregate student mastery
SELECT cron.schedule(
  'nightly-mastery-aggregation',
  '0 0 * * *', -- Run at midnight every day
  $$
    -- Example PL/pgSQL function call that would aggregate data
    -- SELECT calculate_mastery_for_all_students();
  $$
);

-- Example: Clean up stale learning sessions every hour
SELECT cron.schedule(
  'cleanup-stale-sessions',
  '0 * * * *',
  $$
    UPDATE "LearningSession"
    SET end_time = now()
    WHERE end_time IS NULL AND start_time < now() - interval '4 hours';
  $$
);
