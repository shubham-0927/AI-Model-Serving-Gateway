from abc import ABC, abstractmethod

class BaseRoutingStrategy(ABC):
    @abstractmethod
    def select_provider(self, providers:list, user_tier:str = "free"):
        pass