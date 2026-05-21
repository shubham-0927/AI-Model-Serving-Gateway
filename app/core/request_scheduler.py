import json

from app.core.metrics import QUEUE_SIZE
from app.core.redis import rate_limit_redis
from app.registry.provider_registry import HIGH_PRIORITY_QUEUE,LOW_PRIORITY_QUEUE


def enqueue_request(payload: dict,user_tier: str):
    queue_name = (
        HIGH_PRIORITY_QUEUE
        if user_tier == "premium"
        else LOW_PRIORITY_QUEUE
    )
    rate_limit_redis.rpush(queue_name,json.dumps(payload))
    QUEUE_SIZE.labels(queue=queue_name).inc()

def get_queue_size(
    queue_name: str
):

    return rate_limit_redis.llen(
        queue_name
    )