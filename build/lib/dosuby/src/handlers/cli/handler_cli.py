from dosuby.src.interfaces.handler import Handler
import logging
from dosuby.src.core.application.decorators.loggers_decorators import *


class HandlerCli(Handler):
    """Handler Interface for Cli implementation

    Args:
        Handler (EnumerationHandler): Abstract class for enumerator handlers
    """
    
    def pre_handler_process(self, **kwargs):
        # Display handler name on the CLI
        # print('+'*20)
        # print(self)
        # print('+'*20)
        logging.info(f"{C}[*] Running enumeration{C} {W}[{self}]{W}")