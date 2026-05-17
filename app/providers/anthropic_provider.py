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

        tokens = [
            "Anthropic",
            "Anthropic streaming",
            "Anthropic streaming response"
        ]

        for token in tokens:

            yield {
                "event": "message",
                "data": token
            }

            await asyncio.sleep(1)