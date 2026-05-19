SIMULATION_CONFIG = {

    "openai": {

        "min_latency_ms": 200,

        "max_latency_ms": 1200,

        "failure_rate": 0.1,

        "stream_chunk_delay": 0.3,
        "degraded": False
    },

    "anthropic": {

        "min_latency_ms": 500,

        "max_latency_ms": 2500,

        "failure_rate": 0.25,

        "stream_chunk_delay": 0.6,
        "degraded": False
    }
}
import asyncio
import random
from prometheus_client import Counter


# Counter for simulated provider failures
SIMULATED_FAILURES = Counter(
    "simulated_provider_failures_total",
    "Total number of simulated provider failures",
    ["provider"],
)


async def simulate_provider_behavior(provider_name: str):

    config = SIMULATION_CONFIG[provider_name]

    latency = random.randint(

        config["min_latency_ms"],

        config["max_latency_ms"]
    )
    if config["degraded"]:
        latency *= 3

    await asyncio.sleep(
        latency / 1000
    )

    if random.random() < (config["failure_rate"]):
        SIMULATED_FAILURES.labels(provider=provider_name).inc()

        raise Exception(

            f"{provider_name} simulated failure"
        )

    return latency