from app.workers.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.job import Job
from datetime import datetime
import time
import json
from app.core.redis import celery_redis
from app.core.config import settings
from app.models.request_log import RequestLog


@celery_app.task
def process_job(job_id: str):
    # print(f"Processing job {job_id}")

    # time.sleep(5)  # simulate long task

    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return
        job.status = "running"
        job.started_at = datetime.utcnow()
        db.commit()

        # just for simulation
        time.sleep(5)

        job.status = "completed"
        job.completed_at = datetime.utcnow()
        job.output_data = "Dummy result of the job!!"
        db.commit()
    except Exception as e:
        # job can be null
        if job:
            job.status = "failed"
            job.error_message = str(e)
            db.commit()

    finally:
        # print()
        db.close()
    return {"status": "completed"}

@celery_app.task
def flush_logs_to_db():
    db = SessionLocal()
    try:
        buffered_logs = []

        while True:
            item = celery_redis.lpop(
                settings.REQUEST_LOG_QUEUE
            )

            if not item:
                break

            buffered_logs.append(json.loads(item))
        if not buffered_logs:
            return "No logs to flush"

        db_objects = [
            RequestLog(**log)
            for log in buffered_logs
        ]
        db.bulk_save_objects(db_objects)
        db.commit()
        return f"Inserted {len(db_objects)} logs"

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()