from app.routing.base_strategy import (
    BaseRoutingStrategy
)

from app.registry.provider_registry import (
    ProviderRegistry
)


class AdaptiveRoutingStrategy(
    BaseRoutingStrategy
):

    def select_provider(
        self,
        providers: list,
        user_tier: str = "free"
    ):

        if not providers:

            raise ValueError(
                "No providers available"
            )

        best_provider = max(

            providers,

            key=lambda provider:
            ProviderRegistry.get_provider_score(
                provider,
                user_tier
            )
        )

        return best_provider