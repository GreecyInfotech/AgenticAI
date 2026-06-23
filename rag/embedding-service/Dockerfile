FROM python:3.11-slim
WORKDIR /app
COPY shared/python/smart_port_common /app/shared/python/smart_port_common
COPY rag/embedding-service /app/rag/embedding-service
RUN pip install -e /app/shared/python/smart_port_common -e /app/rag/embedding-service
COPY rag/embedding-service/src /app/src
ENV PYTHONPATH=/app/src
EXPOSE 8202
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8202", "--app-dir", "/app/src"]
