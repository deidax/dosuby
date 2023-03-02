import socket
from src.adapter.ports_scanning.socket_port_scanning_adapter import SocketPortScanningAdapter
from src.adapter.cms_scanning.wordpress_scanning_adapter import WordPressScanningAdapter
from src.core.domain.cache import Cache
from src.core.domain.enumeration_reporte import EnumerationReporte
import logging
try:
    from urllib.parse import urlparse
except ImportError:
    print("No module named 'urllib' found")

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
        cached_result = cache.check_if_ip_already_found_and_return_result(ip=value.get('ip'))
        if cached_result:
            return cached_result.get('open_ports')
        
        
        try:
            port_scanning = SocketPortScanningAdapter()
            port_scanning.target_uri = value.get('uri')
            return port_scanning.run()
        except:
            pass
        
        return []
    return wrapper



def cache_subdomain(func):
    def wrapper(self, value):
        try:
            cache_singleton = Cache()
            cache_singleton.add(value.get_cached_data())
        except Exception as exc:
            raise exc
        
        func(self, value)
    return wrapper

def save_enumeration_report(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        
        try:
            report_singleton = EnumerationReporte()
            report_singleton.add(value)
        except:
            pass
        
        return value
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



def scan_for_cms(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        
        try:
            cms = None
            cache_singleton = Cache()
            cached_result = cache_singleton.check_if_ip_already_found_and_return_result(ip=value.get('ip'))
            if 80 in cached_result.get('open_ports'):
                cms_scanning_adapter = WordPressScanningAdapter()
                cms_scanning_adapter.subdomain_uri = value.get('uri')
                cms = cms_scanning_adapter.run()
        except:
            cms = None
        
        return cms
    return wrapper

def save_cms(attr_name):
    """values in a list

    Args:
        attr_name (list): list attribute to append to
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            cms = func(*args, **kwargs)
            setattr(args[0], attr_name, cms)
            return cms
        return wrapper
    return decorator