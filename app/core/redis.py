import redis
from app.core.config import settings

# redis_client = redis.Redis(
#     host=settings.REDIS_HOST,
#     port=settings.REDIS_PORT,
#     decode_responses=True
# )

rate_limit_redis = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_RATE_LIMIT_DB,
    decode_responses=True
)

celery_redis = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_CELERY_DB,
    decode_responses=True
)