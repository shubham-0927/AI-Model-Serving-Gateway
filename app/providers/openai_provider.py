import asyncio
import random

from app.providers.base_provider import BaseProvider
class OpenAIProvider(BaseProvider):
    # async def generate_response(self, prompt: str):
    #     # return await super().generate_response(prompt)
    #     await asyncio.sleep(1)
    #     return {"provider": "openai",
    #             "response":f"OpenAI mock response for: {prompt}"}

    async def generate_response(
        self,
        prompt: str
    ):

        await asyncio.sleep(1)

        # Simulate random provider failure
        if random.random() < 0.5:

            raise Exception(
                "OpenAI provider unavailable"
            )

        return {
            "provider": "openai",
            "response": (
                f"OpenAI mock response for: {prompt}"
            )
        }


    async def stream_response(self, prompt:str):
        tokens = [
            "OpenAI",
            "OpenAI streaming",
            "OpenAI streaming response"
        ]
        for token in tokens:
            yield{
                "event":"message",
                "data":token
            }
            await asyncio.sleep(1)