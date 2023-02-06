from src.interfaces.handler import Handler
from abc import abstractmethod
from typing import Any

class DefaultHandler(Handler):
    
    _next_handler: Handler = None
    
    def set_next(self, handler: Handler) -> Handler:
        """Returning a handler from here will let us link handlers in a
            convenient way like this:\n
            google_dork_handler.set_next(yahoo_dork_handler)

        Args:
            handler (Handler): Handler name

        Returns:
            Handler: next handler to be use
        """
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, uri: str):
        if self._next_handler:
            return self._next_handler.handle(uri)

        return None
