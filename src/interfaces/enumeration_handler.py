from abc import ABC, abstractmethod

class EnumerationHandler(ABC):
    """
    The Handler interface declares a method for building the chain of subdomain handlers.
    """


    @abstractmethod
    def handle(self, uri: str):
        pass