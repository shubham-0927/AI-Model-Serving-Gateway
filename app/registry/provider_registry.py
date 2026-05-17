# PROVIDER_REGISTRY = {

#     "openai": {

#         "models": [
#             "gpt-4",
#             "gpt-3.5"
#         ],

#         "healthy": True,

#         "supports_streaming": True,

#         "cost_tier": "high",

#         "failure_count": 0
#     },

#     "anthropic": {

#         "models": [
#             "claude-3",
#             "gpt-3.5"
#         ],

#         "healthy": True,

#         "supports_streaming": True,

#         "cost_tier": "medium",

#         "failure_count": 0
#     }
# }

from app.core.redis import (
    rate_limit_redis
)
import time

HEALTH_KEY = "provider:{provider}:healthy"

FAILURE_KEY = (
    "provider:{provider}:failure_count"
)


COOLDOWN_KEY = (
    "provider:{provider}:cooldown_until"
)


PROVIDER_METADATA = {


    "openai": {

        "models": [
            "gpt-4",
            "gpt-3.5"
        ],

        "supports_streaming": True,

        "cost_tier": "high"
    },

    "anthropic": {

        "models": [
            "claude-3",
            "gpt-3.5"
        ],

        "supports_streaming": True,

        "cost_tier": "medium"
    }
}


# class ProviderRegistry:

#     @staticmethod
#     def get_provider_info(
#         provider_name: str
#     ):

#         return PROVIDER_REGISTRY.get(
#             provider_name
#         )

#     @staticmethod
#     def is_healthy(
#         provider_name: str
#     ):

#         provider = (
#             PROVIDER_REGISTRY.get(
#                 provider_name
#             )
#         )

#         if not provider:
#             return False

#         return provider["healthy"]

#     @staticmethod
#     def mark_failure(
#         provider_name: str
#     ):

#         provider = (
#             PROVIDER_REGISTRY.get(
#                 provider_name
#             )
#         )

#         if not provider:
#             return

#         provider["failure_count"] += 1

#         if provider["failure_count"] >= 3:

#             provider["healthy"] = False

#     @staticmethod
#     def reset_failures(
#         provider_name: str
#     ):

#         provider = (
#             PROVIDER_REGISTRY.get(
#                 provider_name
#             )
#         )

#         if not provider:
#             return

#         provider["failure_count"] = 0

#         provider["healthy"] = True

#     @staticmethod
#     def get_healthy_providers():

#         return [

#             provider_name

#             for provider_name, metadata

#             in PROVIDER_REGISTRY.items()

#             if metadata["healthy"]
#         ]
    
#     @staticmethod
#     def get_providers_for_model(
#         model_name: str
#     ):

#         matching_providers = []

#         for provider_name, metadata in (
#             PROVIDER_REGISTRY.items()
#         ):

#             if (
#                 model_name
#                 in metadata["models"]
#             ) and metadata["healthy"]:

#                 matching_providers.append(
#                     provider_name
#                 )

#         return matching_providers

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