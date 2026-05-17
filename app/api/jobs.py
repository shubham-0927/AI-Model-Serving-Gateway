from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app.db.session import get_db
from app.core.api_key_auth import get_api_key
from app.models.api_key import APIKey
from app.models.job import Job
from app.services.job_services import create_job
from app.workers.tasks import process_job

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/")
def submit_job(
    api_key: APIKey = Depends(get_api_key),
    db: Session = Depends(get_db)
):
    job = create_job(db, api_key.user_id, api_key.id)
    process_job.delay(job.id)
    return {"job_id": job.id, "status": "queued"}

@router.get("/{job_id}")
def get_job(
    job_id: str,
    api_key: APIKey = Depends(get_api_key),
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.api_key_id == api_key.id
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job.id,
        "status": job.status,
        "result": job.output_data,
        "error": job.error_message
    }