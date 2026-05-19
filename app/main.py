from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api import auth, keys, gateway
from app.api import jobs

# Import all models to register them with Base.metadata
from app.models.user import User
from app.models.api_key import APIKey
from app.models.job import Job
from app.api import usage
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from fastapi.responses import Response
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from app.core.tracing import tracer

app = FastAPI(title="Ai Model Serving Gateway")
app.include_router(auth.router)
app.include_router(keys.router)
app.include_router(gateway.router)
app.include_router(jobs.router)
app.include_router(usage.router)

FastAPIInstrumentor.instrument_app(app)

@app.get("/health")
async def health():
    return {"status":"ok"}

@app.get("/health/db")
def db_health(db: Session = Depends(get_db)):
    return {"db": "connected"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type= CONTENT_TYPE_LATEST)