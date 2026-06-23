FROM python:3.11-slim
WORKDIR /app
COPY shared/python/smart_port_common /app/shared/python/smart_port_common
COPY mcp-servers/kafka-mcp /app/mcp-servers/kafka-mcp
RUN pip install -e /app/shared/python/smart_port_common -e /app/mcp-servers/kafka-mcp
COPY mcp-servers/kafka-mcp/src /app/src
ENV PYTHONPATH=/app/src
CMD ["python", "/app/src/server.py"]
