FROM python:3.11-slim
WORKDIR /app
COPY shared/python/smart_port_common /app/shared/python/smart_port_common
COPY rag/chunking /app/rag/chunking
RUN pip install -e /app/shared/python/smart_port_common -e /app/rag/chunking
COPY rag/chunking/src /app/src
ENV PYTHONPATH=/app/src
EXPOSE 8201
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8201", "--app-dir", "/app/src"]
