from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)
celery_app.conf.beat_schedule = {

    "flush-logs-every-10-seconds": {

        "task":
        "app.workers.tasks.flush_logs_to_db",

        "schedule": 10.0
    },

    "process-queued-requests": {

        "task":
        "app.workers.tasks.process_queued_requests",

        "schedule": 2.0
    }
}

celery_app.conf.timezone = "UTC"
import app.workers.tasks
