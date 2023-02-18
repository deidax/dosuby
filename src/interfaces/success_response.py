from .search_response import SearchResponse
from src.core.application.enums.cli_response_type_enum import CliResponseTypeEnums
from src.core.domain.target import Target

class SuccessResponse(SearchResponse):
    """Successful search result.
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.status_code = CliResponseTypeEnums.SUCCESS['status_code']
        self.response_type = CliResponseTypeEnums.SUCCESS
    
    def get_response(self):
        response = {
            'type': self.response_type,
            'status_code': self.status_code,
            'message': self.response_message,
            'subdomain': self.target.subdomain.subdomain_uri
        }
        
        return f"Status:    {response.get('status_code')}\n"\
               f"Message:   {response.get('message')}\n"\
               f"Subdomain: {response.get('subdomain')}\n"\
               f"{'-'*10}\n"
        
    def get_target_subdomains(self):
        if self.target:
            return self.target.get_target_intel()
        return []
    
    def set_target(self, target: Target):
        return super().set_target(target)
        
