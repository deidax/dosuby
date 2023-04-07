import socket
from src.adapter.ports_scanning.socket_port_scanning_adapter import SocketPortScanningAdapter
from src.core.domain.cache import Cache
from src.core.domain.config import Config
from src.core.application.enums.modules_status import ModuleStatus
from src.core.domain.enumeration_reporte import EnumerationReporte
from src.adapter.cms_scanning.wordpress_scanning_adapter import WordPressScanningAdapter
from src.adapter.webserver_scanning.http_client_webserver_scanning_adapter import HttpClientWebserverScanningAdapter
from .loggers_decorators import *



def get_ip(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        config = Config()
        if not config.scanning_modules:
            return ModuleStatus.ABORT

        try:
            value = socket.gethostbyname(value)
        except:
            value = None
        
        return value
    return wrapper

def get_hostname(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        config = Config()
        if not config.scanning_modules:
            return ModuleStatus.ABORT
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
        config = Config()
        if not config.scanning_modules:
            return ModuleStatus.ABORT
        # check if the ip address is already in the cache
        cache = Cache()
        cached_result = cache.check_if_ip_already_found_and_return_result(ip=value.get('ip'))
        display_sub_info = True
        if cached_result:
            c_r = cached_result.get('open_ports')
            display_sub_info = True
            return c_r
        
        if display_sub_info:
            log_subdomain_info(f"--> {value.get('ip')}")
        
        loader = Loader("Ports Scanning...").start()
        loader.end = "Ports Scanning -> [DONE]"
        
        try:
            port_scanning = SocketPortScanningAdapter()
            port_scanning.target_uri = value.get('uri')
            ports = port_scanning.run()
            loader.stop()
            return ports
        except:
            pass
        
        loader.stop()
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

def scan_for_cms(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        config = Config()
        if not config.scanning_modules:
            return ModuleStatus.ABORT
        
        loader = Loader("CMS Scanning...").start()
        loader.end = "CMS Scanning -> [DONE]"
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
        
        loader.stop()
        return cms
    return wrapper

def save_cms(attr_name):
    """values in a list

    Args:
        attr_name (list): list attribute to append to
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            config = Config()
            if not config.scanning_modules:
                return ModuleStatus.ABORT
            cms = func(*args, **kwargs)
            setattr(args[0], attr_name, cms)
            return cms
        return wrapper
    return decorator

def get_webserver(func):
    """Scan for webserver

    Args:
        func (Any): function that raturn a subdomain
    """
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        config = Config()
        if not config.scanning_modules:
            return ModuleStatus.ABORT
        
        loader = Loader("Webserver Scanning...").start()
        loader.end = "Webserver Scanning -> [DONE]"
        try:
            cache_singleton = Cache()
            cached_result = cache_singleton.check_if_ip_already_found_and_return_result(ip=value.get('ip'))
            if 80 in cached_result.get('open_ports'):
                webserver_scanning = HttpClientWebserverScanningAdapter()
                webserver_scanning.target_uri = value.get('ip')
                w_s = webserver_scanning.run()
                loader.stop()
                return w_s
        except:
            pass
        
        loader.stop()
        return []
    return wrapper