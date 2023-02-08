from abc import ABC, abstractmethod
from src.interfaces.enumeration_handler import EnumerationHandler

class Handler(EnumerationHandler):
    """
    The Handler interface declares a method for building the chain of subdomain handlers.
    """

    def __init__(self, next_handler: EnumerationHandler=None) -> None:
        self._next_handler = next_handler

    @abstractmethod
    def handle(self, uri: str):
        if self._next_handler:
            return self._next_handler.handle(uri)
        return uri