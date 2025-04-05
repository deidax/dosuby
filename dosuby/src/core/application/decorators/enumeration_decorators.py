import socket
from dosuby.src.adapter.cms_scanning.drupal_scanning_adapter import DrupalScanningAdapter
from dosuby.src.adapter.cms_scanning.joomia_scanning_adapter import JoomlaScanningAdapter
from dosuby.src.adapter.cms_scanning.moodle_scanning_adapter import MoodleScanningAdapter
from dosuby.src.adapter.cms_scanning.wordpress_scanning_adapter import WordPressScanningAdapter
from dosuby.src.adapter.ports_scanning.socket_port_scanning_adapter import SocketPortScanningAdapter
from dosuby.src.adapter.webserver_scanning.apache_webserver_scanning_adapter import ApacheWebServerScanningAdapter
from dosuby.src.adapter.webserver_scanning.generic_webserver_scanning_adapter import GenericWebServerScanningAdapter
from dosuby.src.adapter.webserver_scanning.iis_webserver_scanning_adapter import IISWebServerScanningAdapter
from dosuby.src.adapter.webserver_scanning.lighthttp_webserver_scanning_adapter import LighttpdWebServerScanningAdapter
from dosuby.src.adapter.webserver_scanning.ngnix_webserver_scanning_adapter import NginxWebServerScanningAdapter
from dosuby.src.core.domain.cache import Cache
from dosuby.src.core.domain.config import Config
from dosuby.src.core.application.enums.modules_status import ModuleStatus
from dosuby.src.core.domain.enumeration_reporte import EnumerationReporte
from dosuby.src.adapter.webserver_scanning.http_client_webserver_scanning_adapter import HttpClientWebserverScanningAdapter
from dosuby.src.factories.vulnerability_checker_factory import VulnerabilityCheckerFactory
from dosuby.src.managers.vulnerability_checker_manager import VulnerabilityCheckerManager
from dosuby.src.utils.helpers import extract_server_name_advanced, extract_version
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
    It also saves any discovered vulnerabilities directly to the Subdomain instance.
    Returns the CMS detection result directly.
    """
    def wrapper(*args, **kwargs):
        # Get the subdomain info from the wrapped function
        value = func(*args, **kwargs)
        
        # Get the Subdomain instance (self) from args
        self = args[0]
        
        config = Config()
        
        if not config.scanning_modules:
            return ModuleStatus.ABORT
            
        try:
            cms = None
            cms_output = "N/A"
            loader = None
            cache_singleton = Cache()
            cached_result = cache_singleton.check_if_ip_already_found_and_return_result(ip=value.get('ip'))
            cached_uri = cache_singleton.check_if_uri_already_found_and_return_result(value.get('uri'))
            
            # Check if we have a cached result for this IP
            cached_result = cache_singleton.check_if_ip_already_found_and_return_result(ip=value.get('ip'))
            
            # Only scan if port 80 is open
            if 80 in cached_result.get('open_ports', []):
                if cached_uri:
                    loader = Loader(f"{Y}       [->] CMS Scanning...{Y}").start()
                    loader.end = f"{Y}       [*] CMS Scanning{Y}{G} [DONE]{G}"
                
                vulnerability_checker = None
                if config.check_cms_vulnerabilities:
                    try:
                        vulnerability_checker = VulnerabilityCheckerManager.get_instance(name='nvd')
                    except Exception as vcf_error:
                        print(f"Error creating vulnerability checker: {vcf_error}")
                
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

                        if cms.get('confidence') != 'Low':
                            
                            if cms.get('version') is not None:
                                cms_version = f" v{cms.get('version')}"
                                
                            cms_output = "{}{} - confidence: {}".format(
                                cms.get('cms'),
                                cms_version,
                                cms.get('confidence')
                            )
                            
                            if config.check_cms_vulnerabilities and vulnerability_checker and cms.get('version'):
                                try:
                                    # Check for vulnerabilities
                                    vulnerabilities = vulnerability_checker.check_cms_vulnerabilities(
                                        cms.get('cms'), cms.get('version')
                                    )
                                    
                                    # Get summary of vulnerabilities
                                    summary = vulnerability_checker.get_vulnerability_summary(vulnerabilities)
                                    # Add vulnerability information to the cms result
                                    cms['vulnerabilities'] = vulnerabilities
                                    cms['vulnerability_summary'] = summary
                                    cms['is_vulnerable'] = summary['has_vulnerabilities']
                                    
                                    # Add vulnerability information to the output string
                                    if summary['has_vulnerabilities']:
                                        vuln_info = f" - VULNERABLE: {summary['total']} issues"
                                        
                                        # Add severity info
                                        if summary['critical'] > 0:
                                            vuln_info += f" ({summary['critical']} critical"
                                            if summary['high'] > 0:
                                                vuln_info += f", {summary['high']} high"
                                            vuln_info += ")"
                                        elif summary['high'] > 0:
                                            vuln_info += f" ({summary['high']} high)"
                                            
                                        # Add exploitable count
                                        if summary['exploitable'] > 0:
                                            vuln_info += f", {summary['exploitable']} exploitable"
                                            
                                        cms_output += vuln_info
                                        
                                    # DIRECT SAVE: Store vulnerabilities in the Subdomain instance
                                    try:
                                        # Check if _vulnerabilities attribute exists
                                        if not hasattr(self, '_vulnerabilities'):
                                            # Attribute doesn't exist - provide a helpful error message
                                            error_msg = (
                                                "Error: '_vulnerabilities' attribute not found in class."
                                                "Please ensure your class defines a '_vulnerabilities' attribute, "
                                                "typically initialized as: _vulnerabilities: List[Dict[str, Any]] = field(init=False, default_factory=list)"
                                            )
                                            print(error_msg)
                                            # Create the attribute as a fallback
                                            setattr(self, '_vulnerabilities', [])
                                        
                                        # Now we can safely store vulnerabilities
                                        for vuln in vulnerabilities:
                                            if vuln not in self._vulnerabilities:
                                                self._vulnerabilities.append(vuln)
                                        
                                    except Exception as e:
                                        print(f"Error saving vulnerabilities to instance: {str(e)}")
                                        
                                except Exception as e:
                                    print(f"Error checking vulnerabilities: {str(e)}")
                            
                        break
            elif cached_uri:
                loader = Loader('').start()
                loader.end = f"{Y}       [*] CMS Scanning{Y}{G} [SKIPED]{G}"
        except Exception as e:
            # Log the exception but don't break the scan
            # print(f"Error in CMS scanning: {str(e)}")
            cms = None
            cms_output = "N/A"
        
        if loader:
            loader.stop()    
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

# def get_webserver(func):
#     """Scan for webserver

#     Args:
#         func (Any): function that raturn a subdomain
#     """
#     def wrapper(*args, **kwargs):
#         value = func(*args, **kwargs)
#         config = Config()
#         if not config.scanning_modules:
#             return ModuleStatus.ABORT
    
#         try:
#             cache_singleton = Cache()
            
#             cached_result = cache_singleton.check_if_ip_already_found_and_return_result(ip=value.get('ip'))
#             cached_uri = cache_singleton.check_if_uri_already_found_and_return_result(value.get('uri'))
#             if 80 in cached_result.get('open_ports'):
                
#                 vulnerability_checker = None
#                 if config.check_webserver_vulnerabilities:
#                     try:
#                         vulnerability_checker = VulnerabilityCheckerManager.get_instance(name='nvd')
#                     except Exception as vcf_error:
#                         print(f"Error creating vulnerability checker: {vcf_error}")
                        
#                 if cached_uri:
#                     loader = Loader(f"{Y}       [->] Webserver Scanning...{Y}").start()
#                     loader.end = f"{Y}       [*] Webserver Scanning{Y}{G} [DONE]{G}"
#                 else:
#                     cache_singleton.add_subdomain_uri(value.get('uri'))
#                 webserver_scanning = HttpClientWebserverScanningAdapter()
#                 webserver_scanning.target_uri = value.get('ip')
#                 w_s = webserver_scanning.run()
#                 loader.stop()
                
#                 return w_s
#             elif cached_uri:
#                 loader = Loader('').start()
#                 loader.end = f"{Y}       [*] Webserver Scanning{Y}{G} [SKIPED]{G}"
#                 loader.stop()
#         except:
#             pass
        
#         return 'N/A'
#     return wrapper

def get_webserver(func):
    """Decorator to scan for webserver and its vulnerabilities
    
    This decorator takes the result of the wrapped function, which should include
    subdomain information, and performs webserver detection on that subdomain.
    It also saves any discovered vulnerabilities directly to the Subdomain instance.
    Returns the webserver detection result directly.
    
    Args:
        func: The function that returns subdomain information
        
    Returns:
        String representation of the webserver or "N/A" if not detected
    """
    def wrapper(*args, **kwargs):
        # Get the subdomain info from the wrapped function
        value = func(*args, **kwargs)
        
        # Get the Subdomain instance (self) from args
        self = args[0]
        
        config = Config()
        if not config.scanning_modules:
            return ModuleStatus.ABORT
        
        loader = None
        
        try:
            # Check cache for existing results
            cache_singleton = Cache()
            cached_result = cache_singleton.check_if_ip_already_found_and_return_result(ip=value.get('ip'))
            cached_uri = cache_singleton.check_if_uri_already_found_and_return_result(value.get('uri'))
            
            # Check if port 80 is open (required for webserver scanning)
            if 80 in cached_result.get('open_ports', []):
                # Initialize vulnerability checker if needed
                vulnerability_checker = None
                if config.check_webserver_vulnerabilities:
                    try:
                        vulnerability_checker = VulnerabilityCheckerManager.get_instance(name='nvd')
                    except Exception as vcf_error:
                        print(f"[red]Error creating vulnerability checker: {vcf_error}[/red]")
                
                # Show loader if this is a new URI
                if cached_uri:
                    # Use improved Loader with Rich styling
                    loader = Loader(f"{Y}       [->] Webserver Scanning...{Y}").start()
                    loader.end = f"{Y}       [*] Webserver Scanning{Y}{G} [DONE]{G}"
                else:
                    cache_singleton.add_subdomain_uri(value.get('uri'))
                
                # Create webserver scanners in priority order
                webserver_scanners = [
                    ApacheWebServerScanningAdapter(),
                    NginxWebServerScanningAdapter(),
                    IISWebServerScanningAdapter(),
                    LighttpdWebServerScanningAdapter(),
                    GenericWebServerScanningAdapter()  # Fallback for other servers
                ]
                
                # Initialize result variables
                server_info = None
                server_output = "N/A"
                
                # Try to detect web server with specialized scanners first
                for scanner in webserver_scanners:
                    scanner.target_uri = value.get('ip')
                    result = scanner.run()
                    
                    if result and result.get('detected'):
                        server_info = result
                        
                        # Only process further if we have reasonable confidence
                        if server_info.get('confidence') != 'Low':
                            server_version = ""
                            if server_info.get('version') is not None:
                                server_version = f" v{server_info.get('version')}"
                            
                            # Create output string with server and version
                            server_output = "{}{}".format(
                                server_info.get('server'),
                                server_version
                            )
                            
                            # Check for vulnerabilities if version is available
                            vulnerabilities_found = False
                            if config.check_webserver_vulnerabilities and vulnerability_checker and server_info.get('version'):
                                try:
                                    # Check for vulnerabilities
                                    vulnerabilities = vulnerability_checker.check_webserver_vulnerabilities(
                                        server_info.get('server'), server_info.get('version')
                                    )
                                    
                                    # Get summary of vulnerabilities
                                    summary = vulnerability_checker.get_vulnerability_summary(vulnerabilities)
                                    
                                    # Add vulnerability information to the server result
                                    server_info['vulnerabilities'] = vulnerabilities
                                    server_info['vulnerability_summary'] = summary
                                    server_info['is_vulnerable'] = summary['has_vulnerabilities']
                                    
                                    # Add vulnerability information to the output string
                                    if summary['has_vulnerabilities']:
                                        vulnerabilities_found = True
                                        vuln_info = f" - VULNERABLE: {summary['total']} issues"
                                        
                                        # Add severity info
                                        if summary['critical'] > 0:
                                            vuln_info += f" ({summary['critical']} critical"
                                            if summary['high'] > 0:
                                                vuln_info += f", {summary['high']} high"
                                            vuln_info += ")"
                                        elif summary['high'] > 0:
                                            vuln_info += f" ({summary['high']} high)"
                                        
                                        # Add exploitable count
                                        if summary['exploitable'] > 0:
                                            vuln_info += f", {summary['exploitable']} exploitable"
                                        
                                        server_output += vuln_info
                                        
                                        # Stop the loader if vulnerabilities are found
                                        if loader:
                                            loader.stop()
                                        
                                    # DIRECT SAVE: Store vulnerabilities in the Subdomain instance
                                    try:
                                        # Check if _vulnerabilities attribute exists
                                        if not hasattr(self, '_vulnerabilities'):
                                            # Attribute doesn't exist - provide a helpful error message
                                            error_msg = (
                                                "Error: '_vulnerabilities' attribute not found in class."
                                                "Please ensure your class defines a '_vulnerabilities' attribute, "
                                                "typically initialized as: _vulnerabilities: List[Dict[str, Any]] = field(init=False, default_factory=list)"
                                            )
                                            print(f"[red]{error_msg}[/red]")
                                            # Create the attribute as a fallback
                                            setattr(self, '_vulnerabilities', [])
                                        
                                        # Now we can safely store vulnerabilities
                                        for vuln in vulnerabilities:
                                            if vuln not in self._vulnerabilities:
                                                self._vulnerabilities.append(vuln)
                                    
                                    except Exception as e:
                                        print(f"[red]Error saving vulnerabilities to instance: {str(e)}[/red]")
                                
                                except Exception as e:
                                    print(f"[red]Error checking vulnerabilities: {str(e)}[/red]")
                            
                        # We found a server, break out of the loop
                        break
                
                # If no server detected by specialized scanners, fall back to basic HTTP client
                if server_output == "N/A":
                    basic_http = HttpClientWebserverScanningAdapter()
                    basic_http.target_uri = value.get('ip')
                    server_header = basic_http.run()
                    
                    if server_header and server_header != "Unknown" and server_header != "N/A":
                        server_output = server_header
                        
                
                # Make sure to stop the loader if it's still running
                if loader:
                    loader.stop()
                
                return server_output
            
            # If port 80 is not open, show skipped message
            elif cached_uri:
                loader = Loader('').start()
                loader.end = f"{Y}       [*] Webserver Scanning{Y}{G} [SKIPED]{G}"
                if loader:
                    loader.stop()
            
        except Exception as e:
            # Only try to stop the loader if it was initialized
            if loader:
                loader.stop()
            print(f"[red]Error in Webserver scanning: {str(e)}[/red]")
        
        return 'N/A'
    
    return wrapper