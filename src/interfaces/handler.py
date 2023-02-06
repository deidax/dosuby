from abc import ABC, abstractmethod
from typing import Any, Optional

class Handler(ABC):
    """
    The Handler interface declares a method for building the chain of subdomain handlers.
    """

    
    
    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, uri: str):
        pass