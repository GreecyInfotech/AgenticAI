FROM python:3.11-slim
WORKDIR /app
COPY shared/python/smart_port_common /app/shared/python/smart_port_common
COPY mcp-servers/crane-mcp /app/mcp-servers/crane-mcp
RUN pip install -e /app/shared/python/smart_port_common -e /app/mcp-servers/crane-mcp
COPY mcp-servers/crane-mcp/src /app/src
ENV PYTHONPATH=/app/src
CMD ["python", "/app/src/server.py"]
