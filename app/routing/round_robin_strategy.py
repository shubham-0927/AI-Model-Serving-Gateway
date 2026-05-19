# from app.routing.base_strategy import BaseRoutingStrategy
# class RoundRobinStrategy(BaseRoutingStrategy):
#     def __init__(self):
#         self.current_index = 0
#     def select_provider(self, providers : list):
#         # return super().select_provider(providers)
#         if not providers:
#             raise ValueError("No providers available")
#         provider = providers[self.current_index]
#         self.current_index = (self.current_index+ 1) % len(providers)
#         return provider

from app.routing.base_strategy import (
    BaseRoutingStrategy
)

from app.core.redis import (
    rate_limit_redis
)


class RoundRobinStrategy(
    BaseRoutingStrategy
):

    REDIS_KEY = (
        "routing:round_robin:index"
    )

    def select_provider(
        self,
        providers: list,
        user_tier: str = "free"
    ):

        if not providers:
            raise ValueError(
                "No providers available"
            )

        current_index = (
            rate_limit_redis.incr(
                self.REDIS_KEY
            ) - 1
        )

        provider = providers[
            current_index % len(providers)
        ]

        return provider