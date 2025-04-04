from dosuby.src.handlers.cli.interruptible_handler import InterruptibleHandler


def make_interruptible(handler_class):
    """
    Factory function to create interruptible versions of handler classes.
    
    Args:
        handler_class: Original handler class
        
    Returns:
        A class that inherits from both the original handler and InterruptibleHandler
    """
    class InterruptibleHandlerImpl(handler_class, InterruptibleHandler):
        def __init__(self, next_handler=None):
            super().__init__(next_handler)
            
        def run_service(self, uri, success_response):
            # Periodically check for interrupts during service execution
            InterruptibleHandler.check_for_interrupt()
            result = handler_class.run_service(self, uri, success_response)
            InterruptibleHandler.check_for_interrupt()
            return result
    
    return InterruptibleHandlerImpl