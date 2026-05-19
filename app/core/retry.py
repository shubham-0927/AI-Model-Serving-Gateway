import asyncio
import random

MAX_RETRIES = 3

async def exponential_backoff(attempt: int,base_delay: float = 0.2,max_delay: float = 3.0):
    delay = min(base_delay * (2 ** attempt), max_delay)
    jitter = random.uniform(0,  0.1)
    await asyncio.sleep(delay + jitter)