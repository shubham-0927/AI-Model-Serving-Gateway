from app.core.redis import (
    rate_limit_redis
)
from app.core.metrics import PROVIDER_HEALTH
import time

HEALTH_KEY = "provider:{provider}:healthy"

FAILURE_KEY = (
    "provider:{provider}:failure_count"
)


COOLDOWN_KEY = (
    "provider:{provider}:cooldown_until"
)
LATENCY_KEY = (
    "provider:{provider}:avg_latency"
)

SUCCESS_KEY = (
    "provider:{provider}:success_count"
)


PROVIDER_METADATA = {


    "openai": {

        "models": [
            "gpt-4",
            "gpt-3.5"
        ],

        "supports_streaming": True,

        # "cost_tier": "high",

        "cost_per_1k_tokens": 10
    },

    "anthropic": {

        "models": [
            "claude-3",
            "gpt-3.5"
        ],

        "supports_streaming": True,

        # "cost_tier": "medium",
        "cost_per_1k_tokens": 6

    }
}


class ProviderRegistry:

    FAILURE_THRESHOLD = 3
    COOLDOWN_SECONDS = 30

    @staticmethod
    def get_provider_info(
        provider_name: str
    ):

        return PROVIDER_METADATA.get(
            provider_name
        )

    @staticmethod
    def is_healthy(provider_name: str):

        ProviderRegistry.recover_provider_if_ready(provider_name)

        key = HEALTH_KEY.format(provider=provider_name)

        value = rate_limit_redis.get(key)

        if value is None:
            return True

        return value == "true"

    @staticmethod
    def mark_failure(provider_name: str):

        failure_key = FAILURE_KEY.format(
            provider=provider_name
        )

        health_key = HEALTH_KEY.format(
            provider=provider_name
        )

        failures = (
            rate_limit_redis.incr(
                failure_key
            )
        )

        if failures >= (
            ProviderRegistry
            .FAILURE_THRESHOLD
        ):            

            rate_limit_redis.set(
                health_key,
                "false"
            )
            PROVIDER_HEALTH.labels(provider=provider_name).set(0)
            cooldown_key = COOLDOWN_KEY.format(
                provider=provider_name
            )

            cooldown_until = (
                time.time()
                + ProviderRegistry.COOLDOWN_SECONDS
            )

            rate_limit_redis.set(
                cooldown_key,
                cooldown_until
            )

    @staticmethod
    def reset_failures(
        provider_name: str
    ):

        failure_key = FAILURE_KEY.format(
            provider=provider_name
        )
        PROVIDER_HEALTH.labels(provider=provider_name).set(1)

        health_key = HEALTH_KEY.format(
            provider=provider_name
        )

        rate_limit_redis.set(
            failure_key,
            0
        )

        rate_limit_redis.set(
            health_key,
            "true"
        )

    @staticmethod
    def get_healthy_providers():

        healthy = []

        for provider_name in (
            PROVIDER_METADATA.keys()
        ):

            if ProviderRegistry.is_healthy(
                provider_name
            ):

                healthy.append(
                    provider_name
                )

        return healthy

    @staticmethod
    def get_providers_for_model(
        model_name: str
    ):

        matching = []

        for provider_name, metadata in (
            PROVIDER_METADATA.items()
        ):

            if (
                model_name
                in metadata["models"]
            ) and ProviderRegistry.is_healthy(
                provider_name
            ):

                matching.append(
                    provider_name
                )

        return matching
    
    @staticmethod
    def recover_provider_if_ready(
        provider_name: str
    ):

        cooldown_key = (
            COOLDOWN_KEY.format(
                provider=provider_name
            )
        )

        cooldown_until = (
            rate_limit_redis.get(
                cooldown_key
            )
        )

        if not cooldown_until:
            return

        cooldown_until = float(
            cooldown_until
        )

        if time.time() >= cooldown_until:

            ProviderRegistry.reset_failures(
                provider_name
            )

            rate_limit_redis.delete(
                cooldown_key
            )

    @staticmethod
    def record_success(

        provider_name: str,

        latency_ms: int
    ):

        latency_key = LATENCY_KEY.format(
            provider=provider_name
        )

        success_key = SUCCESS_KEY.format(
            provider=provider_name
        )

        current_latency = (
            rate_limit_redis.get(latency_key)
        )

        if current_latency:

            current_latency = float(
                current_latency
            )

            avg_latency = (
                current_latency * 0.7
                + latency_ms * 0.3
            )

        else:

            avg_latency = latency_ms

        rate_limit_redis.set(
            latency_key,
            avg_latency
        )

        rate_limit_redis.incr(
            success_key
        )
    @staticmethod
    def get_provider_score(
        provider_name: str,
        user_tier: str = "free"
    ):

        if not ProviderRegistry.is_healthy(
            provider_name
        ):

            return -1

        latency_key = LATENCY_KEY.format(
            provider=provider_name
        )

        success_key = SUCCESS_KEY.format(
            provider=provider_name
        )

        latency = (
            rate_limit_redis.get(latency_key)
        )

        success_count = (
            rate_limit_redis.get(success_key)
        )

        latency = float(latency or 1000)

        success_count = int(success_count or 1)

        # score = (
        #     success_count / latency
        # )

        metadata = (
            PROVIDER_METADATA[
                provider_name
            ]
        )

        cost = metadata[
            "cost_per_1k_tokens"
        ]

        failures = (
            ProviderRegistry.get_failure_count(
                provider_name
            )
        )
        weights = (ProviderRegistry.get_routing_weights(user_tier))

        # latency_weight = 0.5

        # reliability_weight = 0.3

        # cost_weight = 0.2
        latency_weight = weights["latency"]

        reliability_weight = (weights["reliability"])

        cost_weight = weights["cost"]

        latency_score = 1 / latency

        reliability_score = (
            success_count / (failures + 1)
        )

        cost_score = 1 / cost

        final_score = (

            latency_weight * latency_score

            + reliability_weight
            * reliability_score

            + cost_weight * cost_score
        )

        return final_score
        # return score
    @staticmethod
    def get_failure_count(
        provider_name: str
    ):

        failure_key = FAILURE_KEY.format(
            provider=provider_name
        )

        failures = (
            rate_limit_redis.get(
                failure_key
            )
        )

        return int(failures or 0)
    
    @staticmethod
    def get_routing_weights(
        user_tier: str
    ):

        if user_tier == "premium":

            return {
                "latency": 0.7,
                "reliability": 0.2,
                "cost": 0.1
            }

        return {

            "latency": 0.4,

            "reliability": 0.2,

            "cost": 0.4
        }