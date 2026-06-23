-- Smart Port AI Platform - PostgreSQL initialization
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Core operational tables
CREATE TABLE IF NOT EXISTS vessels (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    imo VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    flag VARCHAR(100),
    teu_capacity INTEGER,
    status VARCHAR(50) DEFAULT 'scheduled',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS berths (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(20) UNIQUE NOT NULL,
    max_length_m DECIMAL(8,2),
    max_draft_m DECIMAL(6,2),
    status VARCHAR(50) DEFAULT 'available',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vessel_calls (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vessel_id UUID REFERENCES vessels(id),
    berth_id UUID REFERENCES berths(id),
    eta TIMESTAMPTZ,
    etd TIMESTAMPTZ,
    ata TIMESTAMPTZ,
    atd TIMESTAMPTZ,
    status VARCHAR(50) DEFAULT 'scheduled',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS containers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    container_number VARCHAR(20) UNIQUE NOT NULL,
    type VARCHAR(10) NOT NULL,
    status VARCHAR(50) DEFAULT 'available',
    yard_location VARCHAR(50),
    vessel_call_id UUID REFERENCES vessel_calls(id),
    weight_kg DECIMAL(10,2),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS customs_declarations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    declaration_number VARCHAR(50) UNIQUE NOT NULL,
    vessel_call_id UUID REFERENCES vessel_calls(id),
    status VARCHAR(50) DEFAULT 'pending',
    risk_score DECIMAL(5,4) DEFAULT 0.0,
    submitted_at TIMESTAMPTZ DEFAULT NOW(),
    cleared_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS invoices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(50) DEFAULT 'draft',
    due_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RAG / Knowledge base
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(500) NOT NULL,
    source VARCHAR(255),
    content_type VARCHAR(100),
    storage_path TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS document_chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_chunks_embedding ON document_chunks
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Audit log
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(255) NOT NULL,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100),
    resource_id VARCHAR(255),
    details JSONB DEFAULT '{}',
    ip_address INET,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_log_user ON audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_created ON audit_log(created_at);

-- Seed data
INSERT INTO berths (code, max_length_m, max_draft_m) VALUES
    ('B-08', 400, 16.0), ('B-12', 350, 14.5), ('B-15', 300, 13.0)
ON CONFLICT DO NOTHING;

INSERT INTO vessels (imo, name, flag, teu_capacity, status) VALUES
    ('9123456', 'MSC Aurora', 'Panama', 14000, 'approaching'),
    ('9234567', 'Maersk Horizon', 'Denmark', 18000, 'scheduled'),
    ('9345678', 'CMA CGM Pacific', 'France', 16000, 'scheduled')
ON CONFLICT DO NOTHING;
