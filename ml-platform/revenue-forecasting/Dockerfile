FROM python:3.11-slim
WORKDIR /app
COPY shared/python/smart_port_common /app/shared/python/smart_port_common
COPY ml-platform/revenue-forecasting /app/ml-platform/revenue-forecasting
RUN pip install -e /app/shared/python/smart_port_common -e /app/ml-platform/revenue-forecasting
COPY ml-platform/revenue-forecasting/src /app/src
ENV PYTHONPATH=/app/src
EXPOSE 8306
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8306", "--app-dir", "/app/src"]
