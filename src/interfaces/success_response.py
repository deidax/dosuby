from .search_response import SearchResponse
from src.core.application.enums.cli_response_type_enum import CliResponseTypeEnums
from src.core.domain.target import Target
from src.core.domain.config import Config
from src.core.application.decorators.loggers_decorators import *
from src.core.application.decorators.loggers_decorators import Loader

class TmpResponse:
    
    def __init__(self, subdomain=None, subdomain_ip=None, subdomain_ports=None, subdomain_cms=None, subdomain_webserver=None) -> None:
        self.subdomain = subdomain
        self.subdomain_ip = subdomain_ip
        self.subdomain_ports = subdomain_ports
        self.subdomain_cms = subdomain_cms
        self.subdomain_webserver = subdomain_webserver
    

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
        response = {
            'type': self.response_type,
            'status_code': self.status_code,
            'message': self.response_message,
            'subdomain': self.target.subdomain.subdomain_uri,
            'subdomain_ip': self.target.subdomain.subdomain_ip,
            'subdomain_ports': self.target.subdomain.subdomain_open_ports_from_uri,
            'subdomain_cms': self.target.subdomain.subdomain_cms,
            'subdomain_webserver': self.target.subdomain.subdomain_webserver,
        }
    
        return f"\n{'-'*20}\n"\
            f"{G}--> {response.get('subdomain')}{G}\n"\
            f"{W}   [+] IP: {response.get('subdomain_ip')}{W}\n"\
            f"{W}   [+] Ports: {response.get('subdomain_ports')}{W}\n"\
            f"{W}   [+] CMS: {response.get('subdomain_cms')}{W}\n"\
            f"{W}   [+] Webserver: {response.get('subdomain_webserver')}{W}\n"\
            f"{'-'*20}\n"
    
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
    
    