from pydantic import BaseModel


class CompletionRequest(BaseModel):

    prompt: str

    model: str | None = None

    provider: str | None = None

    strategy: str | None = "round_robin"

    strict_provider: bool = False
    
    stream: bool = False