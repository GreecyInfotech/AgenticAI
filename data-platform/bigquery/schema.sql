-- BigQuery analytics schema for Smart Port AI Platform

CREATE SCHEMA IF NOT EXISTS smart_port_analytics;

-- Daily operational KPIs
CREATE TABLE IF NOT EXISTS smart_port_analytics.daily_kpis (
  date DATE NOT NULL,
  vessel_calls INT64,
  teu_handled INT64,
  avg_turnaround_hours FLOAT64,
  gate_throughput INT64,
  crane_utilization_pct FLOAT64,
  customs_clearance_rate_pct FLOAT64,
  safety_incidents INT64,
  revenue_usd FLOAT64,
  yard_utilization_pct FLOAT64
);

-- Vessel delay predictions vs actuals
CREATE TABLE IF NOT EXISTS smart_port_analytics.vessel_delay_predictions (
  prediction_id STRING NOT NULL,
  vessel_id STRING NOT NULL,
  predicted_delay_hours FLOAT64,
  actual_delay_hours FLOAT64,
  model_version STRING,
  predicted_at TIMESTAMP,
  features JSON
);

-- Agent invocation analytics
CREATE TABLE IF NOT EXISTS smart_port_analytics.agent_invocations (
  invocation_id STRING NOT NULL,
  agent_name STRING NOT NULL,
  user_id STRING,
  query_length INT64,
  tools_used ARRAY<STRING>,
  confidence FLOAT64,
  latency_ms INT64,
  invoked_at TIMESTAMP
);

-- Revenue forecasting
CREATE TABLE IF NOT EXISTS smart_port_analytics.revenue_forecasts (
  forecast_date DATE NOT NULL,
  forecast_month DATE NOT NULL,
  predicted_revenue_usd FLOAT64,
  actual_revenue_usd FLOAT64,
  model_version STRING,
  features JSON
);
