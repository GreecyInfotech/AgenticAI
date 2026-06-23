FROM python:3.11-slim
WORKDIR /app
COPY shared/python/smart_port_common /app/shared/python/smart_port_common
COPY ml-platform/crane-failure-prediction /app/ml-platform/crane-failure-prediction
RUN pip install -e /app/shared/python/smart_port_common -e /app/ml-platform/crane-failure-prediction
COPY ml-platform/crane-failure-prediction/src /app/src
ENV PYTHONPATH=/app/src
EXPOSE 8302
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8302", "--app-dir", "/app/src"]
