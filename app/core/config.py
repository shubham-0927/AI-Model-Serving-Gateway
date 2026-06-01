import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database - Required in production
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is required")
    
    # Security - Required in production
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY or SECRET_KEY == "supersecret":
        raise ValueError("SECRET_KEY environment variable is required and must be changed from default")
    
    ALGORITHM = "HS256"

    # Redis Configuration
    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    
    REQUEST_LOG_QUEUE = os.getenv("REQUEST_LOG_QUEUE", "request_log_queue")
    
    REDIS_RATE_LIMIT_DB = int(os.getenv("REDIS_RATE_LIMIT_DB", "0"))
    REDIS_CELERY_DB = int(os.getenv("REDIS_CELERY_DB", "1"))
    
    # Celery/RabbitMQ Configuration
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@rabbitmq:5672//")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")
    
    # Application Environment
    APP_ENV = os.getenv("APP_ENV", "development")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    WORKERS = int(os.getenv("WORKERS", "4"))


settings = Settings()