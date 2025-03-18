from dosuby.src.core.domain.target import Target
from dosuby.src.interfaces.security_enumeration import SecurityEnumeration

class PortsEnumerationUseCase:
    """This is the Ports Enumeration Use Case.\n
    it will be used to enumerate open ports of a subdomain
    """
    
    def __init__(self, security_enumerator: SecurityEnumeration) -> None:
        """Inject a search engine dork to be used

        Args:
            security_enumerator (SecurityEnumeration): security_enumerator .Must implement SecurityEnumeration interface
        """
        
        if not isinstance(security_enumerator, SecurityEnumeration):
            raise ValueError(f'security_enumerator param should be a SecurityEnumeration instance, not a {type(security_enumerator)}')
        
        self._security_enumerator = security_enumerator
    
    def execute(self, target: Target):
        """Execute method will run the enumeration process

        Args:
            target (Target): url or domain to enumerate
        """
        if not isinstance(target, Target):
            raise ValueError(f'target param should be a Target instance, not a {type(target)}.')
        self._security_enumerator.target_uri = target.target_uri.uri
        
        return self._security_enumerator.run()
    