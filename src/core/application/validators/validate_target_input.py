from typing import Union
import re

class ValidateTargetInput:
    """Validate the user input before starting the subdomains enumeration
    """
    
    @classmethod
    def extract_domain(self, target: str) -> Union[str, bool] :
        """Extract the domain name from target.\n
        if target is not valid return false

        Args:
            target (str): target string (ex: http://www.example.com, https://www.example.com, ftp://www.example.com, exemple.come)

        Returns:
            str: target domain name
            bool: False if target is not valid
        """
        pattern = re.compile(r'(?:https?://)?(?:www\.)?([\w-]+\.[\w-]+)')
        
        match = pattern.search(target)
        
        return match.group(1) if match else False