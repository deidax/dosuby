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


def extract_server_name(server_header):
    """
    Extract clean server name from a server header string
    
    Args:
        server_header (str): Server header string (e.g., "Apache/2.4.51")
        
    Returns:
        str: Clean server name without version
    """
    if not server_header or server_header in ("Unknown", "N/A"):
        return None
    
    # Common server name patterns
    patterns = {
        r'apache(?:/|\ )': "Apache",
        r'nginx(?:/|\ )': "Nginx",
        r'(?:microsoft-)?iis(?:/|\ )': "IIS",
        r'lighttpd(?:/|\ )': "Lighttpd",
        r'cherokee(?:/|\ )': "Cherokee",
        r'litespeed(?:/|\ )': "LiteSpeed",
        r'caddy(?:/|\ )': "Caddy",
        r'tomcat(?:/|\ )': "Tomcat",
        r'jetty(?:/|\ )': "Jetty"
    }
    
    # Try to match known server patterns
    for pattern, name in patterns.items():
        if re.search(pattern, server_header, re.IGNORECASE):
            return name
    
    # Generic extraction for unknown servers
    # Extract server name before version number
    generic_match = re.match(r'^([a-zA-Z\-_]+)(?:/|\ )', server_header)
    if generic_match:
        return generic_match.group(1).strip()
    
    # If no version separator, return the whole string
    return server_header.strip()

def extract_server_version(server_header):
    """
    Extract version from a server header string
    
    Args:
        server_header (str): Server header string (e.g., "Apache/2.4.51")
        
    Returns:
        str: Version string or None if not found
    """
    if not server_header or server_header in ("Unknown", "N/A"):
        return None
    
    # Version extraction patterns
    patterns = [
        r'(?:/|\ )([\d\.]+)',  # Standard version format: Apache/2.4.51
        r'(?:/|\ )v([\d\.]+)'  # v prefix format: nginx/v1.21.3
    ]
    
    for pattern in patterns:
        match = re.search(pattern, server_header)
        if match:
            return match.group(1)
    
    return None

def normalize_server_info(server_header):
    """
    Extract and normalize server name and version from header
    
    Args:
        server_header (str): Server header string
        
    Returns:
        dict: Normalized server information
    """
    if not server_header or server_header in ("Unknown", "N/A"):
        return {
            "server": None,
            "version": None,
            "raw_header": server_header
        }
    
    server_name = extract_server_name(server_header)
    server_version = extract_server_version(server_header)
    
    return {
        "server": server_name,
        "version": server_version,
        "raw_header": server_header
    }