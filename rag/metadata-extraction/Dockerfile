FROM python:3.11-slim
WORKDIR /app
COPY shared/python/smart_port_common /app/shared/python/smart_port_common
COPY rag/metadata-extraction /app/rag/metadata-extraction
RUN pip install -e /app/shared/python/smart_port_common -e /app/rag/metadata-extraction
COPY rag/metadata-extraction/src /app/src
ENV PYTHONPATH=/app/src
EXPOSE 8204
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8204", "--app-dir", "/app/src"]
