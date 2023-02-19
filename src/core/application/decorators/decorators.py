import socket
from src.adapter.ports_scanning.socket_port_scanning_adapter import SocketPortScanningAdapter

def get_ip(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        
        try:
            value = socket.gethostbyname(value)
        except:
            pass
        
        return value
    return wrapper

def get_hostname(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        
        try:
            value = socket.gethostbyaddr(value)[0]
        except socket.error:
            value = "No reverse DNS record found"
        
        return value
    return wrapper

def get_open_ports(func):
    """Scan for open ports

    Args:
        func (Any): function that raturn a domain name
    """
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        
        try:
            port_scanning = SocketPortScanningAdapter()
            port_scanning.target_uri = value
            return port_scanning.run()
        except:
            pass
        
        return []
    return wrapper

def save_open_port(attr_name):
    """Store open ports in a list

    Args:
        attr_name (list): list attribute to append to
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            setattr(args[0], attr_name, result)
            return result
        return wrapper
    return decorator