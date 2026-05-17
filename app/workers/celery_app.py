from celery import Celery
from app.core.config import settings

redis_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_CELERY_DB}"
celery_app = Celery("worker", broker=redis_url, backend=redis_url)
celery_app.conf.beat_schedule = {
    "flush-logs-every-10-seconds": {
        "task": "app.workers.tasks.flush_logs_to_db",
        "schedule": 10.0
    }
}
celery_app.conf.timezone = "UTC"
import app.workers.tasks
