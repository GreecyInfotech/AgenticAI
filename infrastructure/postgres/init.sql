-- PostgreSQL schema for AI Distributor Ordering Platform

CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    tier VARCHAR(32) NOT NULL DEFAULT 'standard',
    credit_limit NUMERIC(12, 2) NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS products (
    sku VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price NUMERIC(12, 2) NOT NULL,
    category VARCHAR(128) NOT NULL DEFAULT 'general',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS inventory (
    sku VARCHAR(64) PRIMARY KEY REFERENCES products(sku),
    available INTEGER NOT NULL DEFAULT 0,
    warehouse VARCHAR(64) NOT NULL DEFAULT 'WH-01',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(64) PRIMARY KEY,
    customer_id VARCHAR(64) NOT NULL REFERENCES customers(customer_id),
    total NUMERIC(12, 2) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'created',
    items JSONB NOT NULL DEFAULT '[]',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);

INSERT INTO customers (customer_id, name, tier, credit_limit) VALUES
    ('CUST-001', 'Demo Distributor', 'gold', 50000.00)
ON CONFLICT (customer_id) DO NOTHING;

INSERT INTO products (sku, name, price, category) VALUES
    ('SKU-001', 'Widget A', 29.99, 'widgets'),
    ('SKU-002', 'Widget B', 49.99, 'widgets'),
    ('SKU-12345', 'Industrial Bearing', 15.50, 'parts')
ON CONFLICT (sku) DO NOTHING;

INSERT INTO inventory (sku, available, warehouse) VALUES
    ('SKU-001', 500, 'WH-01'),
    ('SKU-002', 200, 'WH-01'),
    ('SKU-12345', 120, 'WH-01')
ON CONFLICT (sku) DO NOTHING;
