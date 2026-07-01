-- Infrastructure support tables (memory, audit)
-- Applied via init.sql; kept here for migration tracking.

CREATE TABLE IF NOT EXISTS outbound_emails (
    email_id VARCHAR(64) PRIMARY KEY,
    recipient VARCHAR(255) NOT NULL,
    subject VARCHAR(512) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'queued',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_outbound_emails_status ON outbound_emails(status);
