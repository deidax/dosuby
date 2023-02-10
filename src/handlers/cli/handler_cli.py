from src.interfaces.handler import Handler


class HandlerCli(Handler):
    """Handler Interface for Cli implementation

    Args:
        Handler (EnumerationHandler): Abstract class for enumerator handlers
    """
    
    def pre_handler_process(self, **kwargs):
        # Display handler name on the CLI
        print('+'*20)
        print(self)
        print('+'*20)