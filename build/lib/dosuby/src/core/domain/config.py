from dataclasses import dataclass, field
from dosuby.src.interfaces.singleton import Singleton



class Config(metaclass=Singleton):
    """Dosuby configuration

    """
    
    scanning_modules: bool = field(init=True, default=False)