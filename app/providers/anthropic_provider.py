import asyncio

from app.providers.base_provider import BaseProvider


class AnthropicProvider(BaseProvider):

    async def generate_response(
        self,
        prompt: str
    ):

        await asyncio.sleep(1)

        return {
            "provider": "anthropic",
            "response": f"Anthropic mock response for: {prompt}"
        }

    async def stream_response(
        self,
        prompt: str
    ):

        words = [
            "This",
            "is",
            "a",
            "streaming",
            "response"
        ]

        for word in words:

            await asyncio.sleep(0.5)

            yield word + " "