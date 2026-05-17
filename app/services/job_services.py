from sqlalchemy.orm import Session
from app.models.job import Job
from datetime import datetime
import uuid

def create_job(db: Session, user_id: str, api_key_id: str):
    job = Job(
        id=str(uuid.uuid4()),
        user_id=user_id,
        api_key_id=api_key_id,
        status="queued",
        created_at=datetime.utcnow()
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    return job