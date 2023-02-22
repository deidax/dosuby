import socket
from src.adapter.ports_scanning.socket_port_scanning_adapter import SocketPortScanningAdapter
from src.core.domain.cache import Cache
from src.core.domain.enumeration_reporte import EnumerationReporte

def get_ip(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        
        try:
            value = socket.gethostbyname(value)
        except:
            value = None
        
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
        # check if the ip address is already in the cache
        cache = Cache()
        print('USING CACHE--->', cache.cache_subdomais)
        if cache.check_if_ip_already_found(ip=value.get('ip')):
            return cache.search_for_ip_port(ip=value)
        
        
        try:
            port_scanning = SocketPortScanningAdapter()
            port_scanning.target_uri = value.get('uri')
            return port_scanning.run()
        except:
            pass
        
        return []
    return wrapper

def add_to_list(attr_name):
    """values in a list

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

# def cache_results(result):
#     cache_singleton = Cache()
#     cache_singleton.cache_subdomains = result
#     return result

def cache_results(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        
        try:
            cache_singleton = Cache()
            cache_singleton.cache_subdomais = value
            # cache_singleton.cache_subdomais = cache_singleton.cache_subdomais
        except:
            pass
        
        return value
    return wrapper

def save_enumeration_report(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        
        try:
            report_singleton = EnumerationReporte()
            report_singleton.report_subdomains = value
        except:
            pass
        
        return value
    return wrapper