from dataclasses import dataclass, field
from dosuby.src.interfaces.singleton import Singleton



class Config(metaclass=Singleton):
    """Dosuby configuration

    """
    
    scanning_modules: bool = field(init=True, default=False)
    
    # Vulnerability scanning configuration
    check_cms_vulnerabilities: bool = field(init=False, default=False)
    vulnerability_checker: str = field(init=True, default="nvd")
    
    # Additional vulnerability scanner options
    return_detailed_vulnerabilities: bool = field(init=True, default=False)