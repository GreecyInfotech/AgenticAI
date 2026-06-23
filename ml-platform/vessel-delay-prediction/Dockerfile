FROM python:3.11-slim
WORKDIR /app
COPY shared/python/smart_port_common /app/shared/python/smart_port_common
COPY ml-platform/vessel-delay-prediction /app/ml-platform/vessel-delay-prediction
RUN pip install -e /app/shared/python/smart_port_common -e /app/ml-platform/vessel-delay-prediction
COPY ml-platform/vessel-delay-prediction/src /app/src
ENV PYTHONPATH=/app/src
EXPOSE 8300
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8300", "--app-dir", "/app/src"]
