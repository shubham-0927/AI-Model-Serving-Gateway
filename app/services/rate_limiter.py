from app.core.redis import rate_limit_redis
from datetime import datetime
TIER_LIMITS = {
    "free":10,
    "pro":100
}

def get_current_window():
    return datetime.utcnow().strftime("%Y-%m-%d-%H-%M")

def check_rate_limit(api_key_id:str, tier:str):
    limit = TIER_LIMITS.get(tier, 10)

    window = get_current_window()
    redis_key = f"rate_limit:{api_key_id}:{window}"
    current = rate_limit_redis.incr(redis_key)
    if current == 1:
        rate_limit_redis.expire(redis_key, 60)
    
    if current > limit:
        return False, limit, current
    return True, limit, current