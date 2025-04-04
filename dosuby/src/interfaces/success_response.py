from .search_response import SearchResponse
from dosuby.src.core.application.enums.cli_response_type_enum import CliResponseTypeEnums
from dosuby.src.core.domain.target import Target
from dosuby.src.core.domain.config import Config
from dosuby.src.core.application.decorators.loggers_decorators import *
from dosuby.infrastructure.libs.loader import Loader
from rich.console import Console
from rich.table import Table


class SuccessResponse(SearchResponse):
    """Successful search result.
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.status_code = CliResponseTypeEnums.SUCCESS['status_code']
        self.response_type = CliResponseTypeEnums.SUCCESS
        self.config = Config()
        self.loader = Loader()
    
    def get_response(self):
        if self.config.scanning_modules is True:
            return self._get_response_with_scanning_modules()
        
        return None
        # return self._get_response_without_scanning_modules()
            
            
    def get_target_subdomains(self):
        if self.target:
            return self.target.get_target_intel()
        return []
    
    def get_target_subdomains_count(self) -> int:
        if self.target:
            return self.target.subdomains_count
        return 0
    
    def set_target(self, target: Target):
        return super().set_target(target)
    
    
    def _get_response_with_scanning_modules(self):
        """
        Aggregate scanning results for a subdomain with robust error handling and formatting.
        
        Returns:
            dict: Structured response with scanning module results
        """
        try:
            # Safely extract subdomain information
            subdomain = self.target.subdomain
            # Define safe extraction helper function
            def safe_extract(attr, formatter=str, default='N/A'):
                """
                Safely extract and format an attribute, with optional formatting.
                
                Args:
                    attr: Attribute to extract
                    formatter (callable): Function to format the attribute
                    default: Default value if attribute is None or empty
                
                Returns:
                    Formatted attribute value or default
                """
                try:
                    value = attr
                    if value is None or (isinstance(value, (list, str)) and len(value) == 0):
                        return default
                    return formatter(value)
                except Exception:
                    return default
            
            # Prepare response dictionary
            response = {
                'type': safe_extract(self.response_type),
                'status_code': safe_extract(self.status_code),
                'message': safe_extract(self.response_message),
                'subdomain': safe_extract(subdomain.subdomain_uri),
                'subdomain_ip': safe_extract(subdomain.subdomain_ip),
                'subdomain_ports': safe_extract(
                    subdomain.subdomain_open_ports_from_uri, 
                    formatter=lambda ports: ", ".join(map(str, ports))
                ),
                'subdomain_cms': safe_extract(subdomain.subdomain_cms),
                'subdomain_webserver': safe_extract(subdomain.subdomain_webserver),
                'subdomain_cve': safe_extract(
                    subdomain.cve_codes, 
                    formatter=lambda cves: ", ".join([
                        f"{cve['cve_id']} (Score: {cve['cvss_score']} | {cve['severity']}{' | Exploitable' if cve.get('exploitable', False) else ''})" 
                        for cve in cves
                    ])
                )
            }
            
            # Prepare columns and row for tabular display
            columns = [
                "Subdomain", 
                "IP", 
                "Open Ports", 
                "CMS", 
                "Web Server", 
                "Vulnerabilities"
            ]
            
            row = [[
                response.get('subdomain', 'N/A'),
                response.get('subdomain_ip', 'N/A'),
                response.get('subdomain_ports', 'N/A'),
                response.get('subdomain_cms', 'N/A'),
                response.get('subdomain_webserver', 'N/A'),
                response.get('subdomain_cve', 'N/A')
            ]]
            
            return {
                'columns': columns,
                'row': row
            }
        
        except Exception as e:
            # Fallback error handling
            print(f"Error in scanning response generation: {e}")
            return {
                'columns': [
                    "Subdomain", 
                    "IP", 
                    "Open Ports", 
                    "CMS", 
                    "Web Server", 
                    "Vulnerabilities"
                ],
                'row': [['Error', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']]
            }
    
    def _get_response_without_scanning_modules(self):
        response = {
            'type': self.response_type,
            'status_code': self.status_code,
            'message': self.response_message,
            'subdomain': self.target.subdomain.subdomain_uri,
        }
    
        return f"\n{'-'*20}\n"\
            f"{C}--> {response.get('subdomain')}{C}\n"\
            f"{'-'*20}\n"
    
    