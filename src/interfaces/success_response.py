from .search_response import SearchResponse
from src.core.application.enums.cli_response_type_enum import CliResponseTypeEnums

class SuccessResponse(SearchResponse):
    """Successful search result Interface"""
    
    def __init__(self) -> None:
        super().__init__()
        self.status_code = CliResponseTypeEnums.SUCCESS['status_code']
        self.response_type = CliResponseTypeEnums.SUCCESS
    
    def get_response(self):
        response = {
            'type': self.response_type,
            'status_code': self.status_code,
            'message': self.response_message,
            'subdomain': self.target.subdomain
        }
        
        return f"Status:    {response.get('status_code')}\n"\
               f"Message:   {response.get('message')}\n"\
               f"Subdomain: {response.get('subdomain')}\n"\
               f"{'-'*10}\n"
        
    def get_target_subdomains(self):
        return self.target.subdomains
        
