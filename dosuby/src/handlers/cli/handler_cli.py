from dosuby.src.interfaces.handler import Handler
import logging
from dosuby.src.core.application.decorators.loggers_decorators import *


class HandlerCli(Handler):
    """Handler Interface for Cli implementation

    Args:
        Handler (EnumerationHandler): Abstract class for enumerator handlers
    """
    def __init__(self, next_handler = None):
        super().__init__(next_handler)
        self.silent = False
    
    def pre_handler_process(self, **kwargs):
        if not self.silent:
            logging.info(f"{C}[*] Running enumeration{C} {W}[{self}]{W}")
        