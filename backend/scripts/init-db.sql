-- backend/scripts/init-db.sql
-- PostgreSQL initialization script

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Create functions for common operations
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for memo_jobs
DROP TRIGGER IF EXISTS update_memo_jobs_updated_at ON memo_jobs;
CREATE TRIGGER update_memo_jobs_updated_at
    BEFORE UPDATE ON memo_jobs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create trigger for memo_results
DROP TRIGGER IF EXISTS update_memo_results_updated_at ON memo_results;
CREATE TRIGGER update_memo_results_updated_at
    BEFORE UPDATE ON memo_results
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create trigger for users
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create views for analytics
CREATE OR REPLACE VIEW v_memo_stats AS
SELECT 
    DATE(created_at) as date,
    COUNT(*) as total_memos,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_memos,
    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_memos,
    AVG(EXTRACT(EPOCH FROM (updated_at - created_at))) as avg_processing_time
FROM memo_jobs
GROUP BY DATE(created_at)
ORDER BY DATE(created_at) DESC;

-- Create view for user activity
CREATE OR REPLACE VIEW v_user_activity AS
SELECT 
    u.id as user_id,
    u.username,
    COUNT(mj.id) as total_memos,
    MAX(mj.created_at) as last_activity,
    AVG(mr.confidence_score) as avg_confidence
FROM users u
LEFT JOIN memo_jobs mj ON mj.id IN (SELECT job_id FROM memo_results WHERE memo_results.job_id = mj.id)
LEFT JOIN memo_results mr ON mr.job_id = mj.id
GROUP BY u.id, u.username
ORDER BY last_activity DESC;

-- Grant permissions
GRANT SELECT ON v_memo_stats TO pitchiq;
GRANT SELECT ON v_user_activity TO pitchiq;

-- Create index for performance
CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_memo_jobs_status_created ON memo_jobs(status, created_at);
CREATE INDEX CONCURRENTLY IF NOT EXISTS ix_memo_results_job_id_created ON memo_results(job_id, created_at);

-- Create function to get memo statistics
CREATE OR REPLACE FUNCTION get_memo_stats(days_back int DEFAULT 30)
RETURNS TABLE(
    total_memos bigint,
    avg_confidence numeric,
    completion_rate numeric,
    avg_processing_seconds numeric
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*)::bigint,
        AVG(mr.confidence_score)::numeric,
        (COUNT(CASE WHEN mj.status = 'completed' THEN 1 END)::numeric / NULLIF(COUNT(*), 0)::numeric * 100)::numeric,
        AVG(EXTRACT(EPOCH FROM (mj.updated_at - mj.created_at)))::numeric
    FROM memo_jobs mj
    LEFT JOIN memo_results mr ON mr.job_id = mj.id
    WHERE mj.created_at >= NOW() - (days_back || ' days')::interval;
END;
$$ LANGUAGE plpgsql;