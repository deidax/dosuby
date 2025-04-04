import socket
import logging
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
from dosuby.src.managers.vulnerability_checker_manager import VulnerabilityCheckerManager
from .loggers_decorators import *
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule

# Create a global console instance for consistent styling
console = Console()

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
            # Use Rich for improved display
            # console.print(f"[bold bright_green]🌐 Subdomain:[/bold bright_green] [bright_green underline]{value.get('uri')}[/bright_green underline]")
            console.print(Rule(f"[bold bright_green]🌐 Subdomain:[/bold bright_green] [bright_green underline]{value.get('uri')}[/bright_green underline]"))
        
        # Use improved Loader with Rich styling
        loader = Loader("Ports Scanning...").start()
        loader.end = "🔍 Ports Scanning"
    
        try:
            port_scanning = SocketPortScanningAdapter()
            port_scanning.target_uri = value.get('uri')
            ports = port_scanning.run()
            
            # If ports are found, display them nicely
            if ports:
                ports_text = ", ".join(str(p) for p in ports)
                # Stop the loader before showing the ports
                loader.stop()
                console.print(Panel(
                    f"[cyan]Found open ports:[/cyan] [green]{ports_text}[/green]",
                    title="Port Scan Results",
                    border_style="cyan"
                ))
            else:
                loader.stop()
            
            return ports
        except Exception as e:
            loader.stop()
            console.print(f"[red]Error scanning ports: {str(e)}[/red]")
        
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
                    # Use improved Loader with Rich styling
                    loader = Loader("CMS Scanning...").start()
                    loader.end = "🔍 CMS Scanning"
                
                vulnerability_checker = None
                if config.check_cms_vulnerabilities:
                    try:
                        vulnerability_checker = VulnerabilityCheckerManager.get_instance(name='nvd')
                    except Exception as vcf_error:
                        console.print(f"[red]Error creating vulnerability checker: {vcf_error}[/red]")
                
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
                            
                            vulnerabilities_found = False
                            
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
                                            
                                        cms_output += vuln_info
                                        
                                        # Stop the loader if vulnerabilities are found
                                        if loader:
                                            loader.stop()
                                            
                                        # Display a nice vulnerability panel
                                        vuln_panel = Panel(
                                            f"[bold red]CMS:[/bold red] {cms.get('cms')}{cms_version}\n"
                                            f"[bold red]Confidence:[/bold red] {cms.get('confidence')}\n"
                                            f"[bold red]Vulnerabilities:[/bold red] {summary['total']} total\n"
                                            f"[bold red]Critical:[/bold red] {summary['critical']}\n"
                                            f"[bold red]High:[/bold red] {summary['high']}\n"
                                            f"[bold red]Exploitable:[/bold red] {summary['exploitable']}",
                                            title="CMS Vulnerabilities Detected",
                                            border_style="red"
                                        )
                                        console.print(vuln_panel)
                                        
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
                                            console.print(f"[red]{error_msg}[/red]")
                                            # Create the attribute as a fallback
                                            setattr(self, '_vulnerabilities', [])
                                        
                                        # Now we can safely store vulnerabilities
                                        for vuln in vulnerabilities:
                                            if vuln not in self._vulnerabilities:
                                                self._vulnerabilities.append(vuln)
                                        
                                    except Exception as e:
                                        console.print(f"[red]Error saving vulnerabilities to instance: {str(e)}[/red]")
                                        
                                except Exception as e:
                                    console.print(f"[red]Error checking vulnerabilities: {str(e)}[/red]")
                            
                            # Display CMS information if confidence is not Low (regardless of vulnerabilities)
                            if loader:
                                loader.stop()
                                
                            # Only display the CMS panel if we haven't already displayed a vulnerability panel
                            if not vulnerabilities_found:
                                console.print(Panel(
                                    f"[cyan]CMS:[/cyan] [green]{cms.get('cms')}{cms_version}[/green]\n"
                                    f"[cyan]Confidence:[/cyan] [green]{cms.get('confidence')}[/green]",
                                    title="CMS Detection Results",
                                    border_style="green"
                                ))
                                
                        break
            elif cached_uri:
                # Use improved Loader for skipped scans
                loader = Loader("", style="bold yellow").start()
                loader.end = "🔍 CMS Scanning (No port 80) [Skipped]"
        except Exception as e:
            # Log the exception but don't break the scan
            cms = None
            cms_output = "N/A"
            console.print(f"[red]Error in CMS scanning: {str(e)}[/red]")
        
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
        
        loader = None
        
        try:
            cache_singleton = Cache()
            cached_result = cache_singleton.check_if_ip_already_found_and_return_result(ip=value.get('ip'))
            cached_uri = cache_singleton.check_if_uri_already_found_and_return_result(value.get('uri'))
            
            if cached_result and 80 in cached_result.get('open_ports', []):
                if cached_uri:
                    # Use improved Loader with Rich styling
                    loader = Loader("Webserver Scanning...").start()
                    loader.end = "🔍 Webserver Scanning "
                else:
                    cache_singleton.add_subdomain_uri(value.get('uri'))
                    
                webserver_scanning = HttpClientWebserverScanningAdapter()
                webserver_scanning.target_uri = value.get('ip')
                w_s = webserver_scanning.run()
                
                # Only stop the loader if it was started
                if loader:
                    loader.stop()
                
                if w_s and w_s != 'N/A':
                    console.print(Panel(
                        f"[magenta]Webserver:[/magenta] [green]{w_s}[/green]",
                        title="Webserver Detection Results",
                        border_style="magenta"
                    ))
                
                return w_s
            elif cached_uri:
                # Use improved Loader for skipped scans
                loader = Loader("").start()
                loader.end = "🔍 Webserver Scanning (No port 80) [Skipped]"
                if loader:  # Check if loader was initialized
                    loader.stop()
            # Add a default case when none of the above conditions match
            else:
                return []
                
        except Exception as e:
            # Only try to stop the loader if it was initialized
            if loader:
                loader.stop()
            console.print(f"[red]Error in Webserver scanning: {str(e)}[/red]")
        
        return 'N/A'
    return wrapper