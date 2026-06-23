"""ML inference service: revenue-forecasting."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel, Field

from smart_port_common import create_health_router, setup_logging, setup_telemetry
from smart_port_common.auth import TokenPayload, verify_token
from smart_port_common.logging import get_logger

from .model import load_model, predict

logger = get_logger(__name__)
SERVICE_NAME = "revenue-forecasting"
SERVICE_PORT = 8306


class PredictionRequest(BaseModel):
    month: float = 0.0
    vessel_calls: float = 0.0
    teu_volume: float = 0.0
    tariff_rate: float = 0.0


class PredictionResponse(BaseModel):
    prediction: float
    confidence: float
    model_version: str = "1.0.0"
    features_used: list[str] = Field(default_factory=lambda: ['month', 'vessel_calls', 'teu_volume', 'tariff_rate'])


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(SERVICE_NAME)
    load_model()
    logger.info("ml_service_started", model="revenue")
    yield


app = FastAPI(title="revenue-forecasting", version="1.0.0", lifespan=lifespan)
app.include_router(create_health_router(SERVICE_NAME))
setup_telemetry(app, SERVICE_NAME)


@app.post("/predict", response_model=PredictionResponse)
async def predict_endpoint(
    request: PredictionRequest, token: TokenPayload = verify_token
) -> PredictionResponse:
    features = request.model_dump()
    result = predict(features)
    return PredictionResponse(**result)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=SERVICE_PORT)
