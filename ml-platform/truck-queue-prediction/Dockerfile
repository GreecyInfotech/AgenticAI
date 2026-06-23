FROM python:3.11-slim
WORKDIR /app
COPY shared/python/smart_port_common /app/shared/python/smart_port_common
COPY ml-platform/truck-queue-prediction /app/ml-platform/truck-queue-prediction
RUN pip install -e /app/shared/python/smart_port_common -e /app/ml-platform/truck-queue-prediction
COPY ml-platform/truck-queue-prediction/src /app/src
ENV PYTHONPATH=/app/src
EXPOSE 8303
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8303", "--app-dir", "/app/src"]
