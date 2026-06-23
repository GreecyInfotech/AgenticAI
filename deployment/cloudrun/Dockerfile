FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY eaap_platform ./eaap_platform
COPY agents ./agents
COPY mcp_servers ./mcp_servers
COPY rag ./rag
COPY vector_store ./vector_store
COPY kafka ./kafka
COPY postgres ./postgres
COPY api-gateway ./api-gateway
COPY agent-gateway ./agent-gateway

RUN pip install --no-cache-dir .

ARG SERVICE_DIR=api-gateway
ARG SERVICE_PORT=8000
ENV SERVICE_DIR=${SERVICE_DIR}
ENV PORT=${SERVICE_PORT}

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT} --app-dir ${SERVICE_DIR}
