import socket
from dosuby.src.adapter.cms_scanning.drupal_scanning_adapter import DrupalScanningAdapter
from dosuby.src.adapter.cms_scanning.joomia_scanning_adapter import JoomlaScanningAdapter
from dosuby.src.adapter.cms_scanning.moodle_scanning_adapter import MoodleScanningAdapter
from dosuby.src.adapter.cms_scanning.wordpress_scanning_adapter import WordPressScanningAdapter
from dosuby.src.adapter.ports_scanning.socket_port_scanning_adapter import SocketPortScanningAdapter
from dosuby.src.core.domain.cache import Cache
from dosuby.src.core.domain.config import Config
from dosuby.src.core.application.enums.modules_status import ModuleStatus
from dosuby.src.core.domain.enumeration_reporte import EnumerationReporte
from dosuby.src.adapter.webserver_scanning.http_client_webserver_scanning_adapter import HttpClientWebserverScanningAdapter
from .loggers_decorators import *

SKIP_LOADING = False

def get_ip(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        config = Config()
        # if not config.scanning_modules:
        #     return ModuleStatus.ABORT

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
        
        cache.add_subdomain_uri(value.get('uri'))
        if display_sub_info:
            logging.info(f"{G}[*]  ==> {value.get('uri')}{G}")
        
        loader = Loader(f"{Y}       [->] Ports Scanning...{Y}").start()
        loader.end = f"{Y}       [*] Ports Scanning{Y}{G} [DONE]{G}"
    
        
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
            cms_output = "N/A"
            cache_singleton = Cache()
            
            # Check if we have a cached result for this IP
            cached_result = cache_singleton.check_if_ip_already_found_and_return_result(ip=value.get('ip'))
            
            # Only scan if port 80 is open
            if 80 in cached_result.get('open_ports', []):
                # Create scanners in priority order
                cms_scanners = [
                    WordPressScanningAdapter(),
                    JoomlaScanningAdapter(),
                    DrupalScanningAdapter(),
                    MoodleScanningAdapter()
                ]
                cms_version = ''
                # Try each CMS scanner until we get a positive detection
                for scanner in cms_scanners:
                    scanner.subdomain_uri = value.get('uri')
                    result = scanner.run()
                    
                        
                    if result and result.get('detected'):
                        cms = result  # Return the full CMS result
                        print("--->", cms)
                        if cms.get('confidence') != 'Low':
                            
                            if cms.get('version') is not None:
                                cms_version = f" v{cms.get('version')}"
                                
                            cms_output = "{}{} - confidence: {}".format(
                                cms.get('cms'),
                                cms_version,
                                cms.get('confidence')
                            )
                        break
            
        except Exception as e:
            # Log the exception but don't break the scan
            # print(f"Error in CMS scanning: {str(e)}")
            cms = None
            cms_output = "N/A"
            
        return cms_output  # Return the CMS result directly
        
    return wrapper

def save_cms(attr_name):
    """values in a list

    Args:
        attr_name (cms): cms attribute to append to
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

def save_webserver(attr_name):
    """values in a list

    Args:
        attr_name (webserver): webserver attribute to append to
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            config = Config()
            if not config.scanning_modules:
                return ModuleStatus.ABORT
            webserver = func(*args, **kwargs)
            setattr(args[0], attr_name, webserver)
            return webserver
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
            cached_uri = cache_singleton.check_if_uri_already_found_and_return_result(value.get('uri'))
            if 80 in cached_result.get('open_ports'):
                if cached_uri:
                    loader = Loader(f"{Y}       [->] Webserver Scanning...{Y}").start()
                    loader.end = f"{Y}       [*] Webserver Scanning{Y}{G} [DONE]{G}"
                else:
                    cache_singleton.add_subdomain_uri(value.get('uri'))
                webserver_scanning = HttpClientWebserverScanningAdapter()
                webserver_scanning.target_uri = value.get('ip')
                w_s = webserver_scanning.run()
                loader.stop()
                return w_s
            elif cached_uri:
                loader = Loader('').start()
                loader.end = f"{Y}       [*] Webserver Scanning (No port 80){Y}{G} [SKIPED]{G}"
                loader.stop()
        except:
            pass
        
        return []
    return wrapper