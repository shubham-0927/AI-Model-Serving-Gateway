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

app = FastAPI(title="Ai Model Serving Gateway")
app.include_router(auth.router)
app.include_router(keys.router)
app.include_router(gateway.router)
app.include_router(jobs.router)
app.include_router(usage.router)

@app.get("/health")
async def health():
    return {"status":"ok"}

@app.get("/health/db")
def db_health(db: Session = Depends(get_db)):
    return {"db": "connected"}