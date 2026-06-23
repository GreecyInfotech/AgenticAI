-- EAAP PostgreSQL schema
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    customer VARCHAR(200) NOT NULL,
    status VARCHAR(30) DEFAULT 'processing',
    total NUMERIC(12, 2) DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO orders (order_number, customer, status, total) VALUES
    ('ORD-1001', 'Acme Corp', 'shipped', 4200.00),
    ('ORD-1002', 'Jane Doe', 'processing', 199.00)
ON CONFLICT DO NOTHING;
