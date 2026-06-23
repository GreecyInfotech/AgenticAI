FROM python:3.11-slim AS base
WORKDIR /app
RUN pip install uv

FROM base AS builder
COPY shared/python/smart_port_common /app/shared/python/smart_port_common
COPY agents/safety-agent /app/agents/safety-agent
COPY pyproject.toml /app/
WORKDIR /app/agents/safety-agent
RUN uv pip install --system -e . -e /app/shared/python/smart_port_common

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY agents/safety-agent/src /app/src
ENV PYTHONPATH=/app/src
EXPOSE 8107
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8107", "--app-dir", "/app/src"]
