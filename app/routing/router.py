from app.routing.round_robin_strategy import (
    RoundRobinStrategy
)
from app.routing.adaptive_routing_strategy import (
    AdaptiveRoutingStrategy
)

from app.registry.provider_registry import ProviderRegistry

class ProviderRouter:

    def __init__(self):

        # self.providers = [
        #     "openai",
        #     "anthropic"
        # ]
        

        self.strategies = {
            "round_robin": RoundRobinStrategy(),
            "latency_aware":AdaptiveRoutingStrategy()
        }

    def get_provider(

        self,

        strategy_name: str,

        model_name: str | None = None,
        user_tier:str = "free"
    ):

        strategy = self.strategies.get(
            strategy_name
        )

        if not strategy:
            raise ValueError(
                f"Unsupported strategy: "
                f"{strategy_name}"
            )

        if model_name:

            healthy_providers = (
                ProviderRegistry
                .get_providers_for_model(
                    model_name
                )
            )

        else:

            healthy_providers = (
                ProviderRegistry
                .get_healthy_providers()
            )

        if not healthy_providers:

            raise ValueError(
                "No healthy providers available"
            )

        return strategy.select_provider(
            healthy_providers,
            user_tier
        )
    
    def get_fallback_chain(
        self,
        primary_provider: str
    ):

        fallback_map = {

            "openai": [
                "openai",
                "anthropic"
            ],

            "anthropic": [
                "anthropic",
                "openai"
            ]
        }

        return fallback_map.get(
            primary_provider,
            [primary_provider]
        )