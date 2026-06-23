FROM python:3.11-slim
WORKDIR /app
COPY shared/python/smart_port_common /app/shared/python/smart_port_common
COPY ml-platform/anomaly-detection /app/ml-platform/anomaly-detection
RUN pip install -e /app/shared/python/smart_port_common -e /app/ml-platform/anomaly-detection
COPY ml-platform/anomaly-detection/src /app/src
ENV PYTHONPATH=/app/src
EXPOSE 8305
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8305", "--app-dir", "/app/src"]
