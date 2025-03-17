from abc import ABC,abstractmethod

class DomainSerializer(ABC):
    
    @staticmethod
    def serialize(uri: str):
        pass