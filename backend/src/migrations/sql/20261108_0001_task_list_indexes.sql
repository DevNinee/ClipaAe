CREATE INDEX IF NOT EXISTS idx_tasks_user_created_at
    ON tasks(user_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_tasks_upload_request_key
    ON tasks ((source_metadata->>'upload_request_key'))
    WHERE source_metadata->>'upload_request_key' IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_generated_clips_task_order
    ON generated_clips(task_id, clip_order);
