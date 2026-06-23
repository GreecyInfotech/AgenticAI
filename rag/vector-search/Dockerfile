FROM python:3.11-slim
WORKDIR /app
COPY shared/python/smart_port_common /app/shared/python/smart_port_common
COPY rag/vector-search /app/rag/vector-search
RUN pip install -e /app/shared/python/smart_port_common -e /app/rag/vector-search
COPY rag/vector-search/src /app/src
ENV PYTHONPATH=/app/src
EXPOSE 8203
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8203", "--app-dir", "/app/src"]
