from dataclasses import dataclass, field
from src.interfaces.singleton import Singleton
from typing import List
from itertools import chain

@dataclass
class Cache(metaclass=Singleton):
    """Cache results to use in real time execution
    """
    
    _cache_subdomais: list = field(init=False, default_factory=list)
    
    
        