FROM python:3.11-slim
WORKDIR /app
COPY shared/python/smart_port_common /app/shared/python/smart_port_common
COPY ml-platform/congestion-prediction /app/ml-platform/congestion-prediction
RUN pip install -e /app/shared/python/smart_port_common -e /app/ml-platform/congestion-prediction
COPY ml-platform/congestion-prediction/src /app/src
ENV PYTHONPATH=/app/src
EXPOSE 8304
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8304", "--app-dir", "/app/src"]
