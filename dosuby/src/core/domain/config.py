from dataclasses import dataclass, field
from dosuby.src.interfaces.singleton import Singleton



@dataclass
class Config(metaclass=Singleton):
    """Dosuby configuration"""
    
    # Basic scanning configuration
    scanning_modules: bool = False
    
    # Vulnerability scanning configuration
    check_cms_vulnerabilities: bool = True
    
    check_webserver_vulnerabilities: bool = True
    
    # Use a default string value directly, not with field()
    vulnerability_checker: str = "nvd"
    
    # Additional vulnerability scanner options
    return_detailed_vulnerabilities: bool = False