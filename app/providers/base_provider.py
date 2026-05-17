from abc import ABC, abstractmethod
class BaseProvider(ABC):
    @abstractmethod
    async def generate_response( self, pprompt:str):
        pass
    @abstractmethod
    async def stream_response(self, prompt:str):
        pass
    