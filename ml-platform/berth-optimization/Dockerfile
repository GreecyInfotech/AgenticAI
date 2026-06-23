FROM python:3.11-slim
WORKDIR /app
COPY shared/python/smart_port_common /app/shared/python/smart_port_common
COPY ml-platform/berth-optimization /app/ml-platform/berth-optimization
RUN pip install -e /app/shared/python/smart_port_common -e /app/ml-platform/berth-optimization
COPY ml-platform/berth-optimization/src /app/src
ENV PYTHONPATH=/app/src
EXPOSE 8301
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8301", "--app-dir", "/app/src"]
