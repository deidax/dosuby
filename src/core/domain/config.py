from dataclasses import dataclass, field
from src.interfaces.singleton import Singleton


@dataclass
class Config(metaclass=Singleton):
    """Dosuby configuration

    """
    
    scanning_modules: bool = field(init=True, default=False)