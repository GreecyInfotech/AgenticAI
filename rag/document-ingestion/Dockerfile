FROM python:3.11-slim
WORKDIR /app
COPY shared/python/smart_port_common /app/shared/python/smart_port_common
COPY rag/document-ingestion /app/rag/document-ingestion
RUN pip install -e /app/shared/python/smart_port_common -e /app/rag/document-ingestion
COPY rag/document-ingestion/src /app/src
ENV PYTHONPATH=/app/src
EXPOSE 8200
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8200", "--app-dir", "/app/src"]
