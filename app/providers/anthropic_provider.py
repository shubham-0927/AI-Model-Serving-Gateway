import asyncio

from app.providers.base_provider import BaseProvider
from app.simulation.provider_simulation import (
    SIMULATION_CONFIG,
    simulate_provider_behavior
)

class AnthropicProvider(BaseProvider):

    async def generate_response(
        self,
        prompt: str
    ):

        # await asyncio.sleep(1)
        latency = await simulate_provider_behavior("anthropic")

        return {
            "provider": "anthropic",
            "response": f"Anthropic mock response for: {prompt}"
        }

    async def stream_response(
        self,
        prompt: str
    ):
        
        config = SIMULATION_CONFIG[
            "anthropic"
        ]

        words = [
            "This",
            "is",
            "a",
            "streaming",
            "response"
        ]

        for word in words:

            # await asyncio.sleep(0.5)
            await asyncio.sleep(config["stream_chunk_delay"])

            yield word + " "