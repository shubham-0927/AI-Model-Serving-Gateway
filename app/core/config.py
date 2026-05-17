import os
from dotenv import load_dotenv

load_dotenv()
class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    ALGORITHM = "HS256"

    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REQUEST_LOG_QUEUE = os.getenv(
        "REQUEST_LOG_QUEUE",
        "request_log_queue"
    )
    REDIS_RATE_LIMIT_DB = int(
    os.getenv("REDIS_RATE_LIMIT_DB", 0)
    )

    REDIS_CELERY_DB = int(
        os.getenv("REDIS_CELERY_DB", 1)
    )


settings = Settings()