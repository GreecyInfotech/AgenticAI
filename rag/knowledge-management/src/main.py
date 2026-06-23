"""Knowledge base CRUD and lifecycle management"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from smart_port_common import create_health_router, setup_logging, setup_telemetry
from smart_port_common.auth import TokenPayload, verify_token
from smart_port_common.logging import get_logger

logger = get_logger(__name__)
SERVICE_NAME = "knowledge-management"
SERVICE_PORT = 8205


class ProcessRequest(BaseModel):
    document_id: str | None = None
    content: str | None = None
    metadata: dict = Field(default_factory=dict)
    options: dict = Field(default_factory=dict)


class ProcessResponse(BaseModel):
    status: str
    document_id: str | None = None
    result: dict = Field(default_factory=dict)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(SERVICE_NAME)
    logger.info("service_starting", service=SERVICE_NAME)
    yield


app = FastAPI(title="knowledge-management", description="Knowledge base CRUD and lifecycle management", version="1.0.0", lifespan=lifespan)
app.include_router(create_health_router(SERVICE_NAME))
setup_telemetry(app, SERVICE_NAME)


@app.post("/process", response_model=ProcessResponse)
async def process(request: ProcessRequest, token: TokenPayload = verify_token) -> ProcessResponse:
    try:
        from .processor import process_document
        result = await process_document(request.model_dump())
        return ProcessResponse(status="success", document_id=request.document_id, result=result)
    except Exception as exc:
        logger.error("process_failed", error=str(exc))
        raise HTTPException(status_code=500, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=SERVICE_PORT)
