"""ML inference service: congestion-prediction."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel, Field

from smart_port_common import create_health_router, setup_logging, setup_telemetry
from smart_port_common.auth import TokenPayload, verify_token
from smart_port_common.logging import get_logger

from .model import load_model, predict

logger = get_logger(__name__)
SERVICE_NAME = "congestion-prediction"
SERVICE_PORT = 8304


class PredictionRequest(BaseModel):
    vessel_count: float = 0.0
    container_moves: float = 0.0
    truck_queue: float = 0.0
    weather_score: float = 0.0


class PredictionResponse(BaseModel):
    prediction: float
    confidence: float
    model_version: str = "1.0.0"
    features_used: list[str] = Field(default_factory=lambda: ['vessel_count', 'container_moves', 'truck_queue', 'weather_score'])


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(SERVICE_NAME)
    load_model()
    logger.info("ml_service_started", model="congestion")
    yield


app = FastAPI(title="congestion-prediction", version="1.0.0", lifespan=lifespan)
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
