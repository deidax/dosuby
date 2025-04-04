import re

def make_interruptible(handler_class):
    """
    Factory function to create interruptible versions of handler classes.
    
    Args:
        handler_class: Original handler class
        
    Returns:
        A class that inherits from both the original handler and InterruptibleHandler
    """
    from dosuby.src.handlers.cli.interruptible_handler import InterruptibleHandler
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




# Basic version number pattern (e.g., 1.2.3)
def extract_version(text):
    pattern = r'\d+(\.\d+)+'
    matches = re.findall(pattern, text)
    return [match for match in re.findall(pattern, text)]

def extract_server_name_advanced(server_string):
    # This handles more complex server strings
    # Matches letters up to the first digit or version indicator
    pattern = r'^([a-zA-Z\s\-_]+?)(?:\s*[\d\.v]|$)'
    match = re.search(pattern, server_string)
    if match:
        return match.group(1).strip()
    return None