import socket
from src.adapter.ports_scanning.socket_port_scanning_adapter import SocketPortScanningAdapter
from src.core.domain.cache import Cache
from src.core.domain.config import Config
from src.core.application.enums.modules_status import ModuleStatus
from src.core.domain.enumeration_reporte import EnumerationReporte
from src.adapter.cms_scanning.wordpress_scanning_adapter import WordPressScanningAdapter
from src.adapter.webserver_scanning.http_client_webserver_scanning_adapter import HttpClientWebserverScanningAdapter



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
    """Decorator to scan for CMS on a given subdomain
    
    This decorator takes the result of the wrapped function, which should include
    subdomain information, and performs CMS detection on that subdomain.
    Returns the CMS detection result directly.
    """
    def wrapper(*args, **kwargs):
        # Get the subdomain info from the wrapped function
        value = func(*args, **kwargs)
        
        config = Config()
        if not config.scanning_modules:
            return ModuleStatus.ABORT
            
        try:
            cms = None
            cache_singleton = Cache()
            
            # Check if we have a cached result for this IP
            cached_result = cache_singleton.check_if_ip_already_found_and_return_result(ip=value.get('ip'))
            
            # Only scan if port 80 is open
            if 80 in cached_result.get('open_ports', []):
                # Create scanners in priority order
                cms_scanners = [
                    WordPressScanningAdapter(),
                    # Uncomment these as you implement them
                    # JoomlaScanningAdapter(),
                    # DrupalScanningAdapter(),
                ]
                
                # Try each CMS scanner until we get a positive detection
                for scanner in cms_scanners:
                    scanner.subdomain_uri = value.get('uri')
                    result = scanner.run()
                    
                    if result and result.get('detected'):
                        cms = result  # Return the full CMS result
                        break
            
        except Exception as e:
            # Log the exception but don't break the scan
            print(f"Error in CMS scanning: {str(e)}")
            cms = None
            
        return cms  # Return the CMS result directly
        
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
        try:
            cache_singleton = Cache()
            cached_result = cache_singleton.check_if_ip_already_found_and_return_result(ip=value.get('ip'))
            if 80 in cached_result.get('open_ports'):
                webserver_scanning = HttpClientWebserverScanningAdapter()
                webserver_scanning.target_uri = value.get('ip')
                return webserver_scanning.run()
        except:
            pass
        
        return []
    return wrapper