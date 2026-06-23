FROM python:3.11-slim
WORKDIR /app
COPY shared/python/smart_port_common /app/shared/python/smart_port_common
COPY mcp-servers/customs-mcp /app/mcp-servers/customs-mcp
RUN pip install -e /app/shared/python/smart_port_common -e /app/mcp-servers/customs-mcp
COPY mcp-servers/customs-mcp/src /app/src
ENV PYTHONPATH=/app/src
CMD ["python", "/app/src/server.py"]
