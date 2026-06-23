FROM python:3.11-slim
WORKDIR /app
COPY shared/python/smart_port_common /app/shared/python/smart_port_common
COPY rag/knowledge-management /app/rag/knowledge-management
RUN pip install -e /app/shared/python/smart_port_common -e /app/rag/knowledge-management
COPY rag/knowledge-management/src /app/src
ENV PYTHONPATH=/app/src
EXPOSE 8205
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8205", "--app-dir", "/app/src"]
