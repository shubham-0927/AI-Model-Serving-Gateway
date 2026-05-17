from app.models.request_log import RequestLog
from datetime import datetime
import time
import json
from app.core.redis import celery_redis
from app.core.config import settings

def create_request_log(
    db,
    user_id,
    api_key_id,
    endpoint,
    method,
    status_code,
    latency_ms,
    tokens_used=0,
    job_id=None
):
    log = RequestLog(
        user_id=user_id,
        api_key_id=api_key_id,
        endpoint=endpoint,
        method=method,
        status_code=status_code,
        latency_ms=latency_ms,
        tokens_used=tokens_used,
        job_id=job_id,
        created_at=datetime.utcnow()
    )

    db.add(log)
    db.commit()
    return log


def queue_request_log(
    user_id,
    api_key_id,
    endpoint,
    method,
    status_code,
    latency_ms,
    tokens_used=0,
    job_id=None
):
    # print("QUEUE LOG FUNCTION CALLED")
    payload = {
        "user_id": user_id,
        "api_key_id": api_key_id,
        "endpoint": endpoint,
        "method": method,
        "status_code": status_code,
        "latency_ms": latency_ms,
        "tokens_used": tokens_used,
        "job_id": job_id,
        "created_at": datetime.utcnow().isoformat()
    }
    celery_redis.rpush(
        settings.REQUEST_LOG_QUEUE,
        json.dumps(payload)
    )