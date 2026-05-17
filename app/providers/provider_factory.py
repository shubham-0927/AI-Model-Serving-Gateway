from app.providers.openai_provider import OpenAIProvider
from app.providers.anthropic_provider import AnthropicProvider

class ProviderFactory:
    @staticmethod
    def get_provider(provider_name: str):
        providers = {
            "openai": OpenAIProvider,
            "anthropic": AnthropicProvider
        }
        provider_class = providers.get(provider_name)
        if not provider_class:
            raise ValueError( f"Unsupported provider: {provider_name}")
        return provider_class()