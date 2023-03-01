from src.interfaces.security_enumeration import SecurityEnumeration

class PortEnumerationAdapter(SecurityEnumeration):
    
    def __init__(self) -> None:
        """This class will manage the port enumeration logic using the Sockets

        """
        super().__init__()
        self._ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443]
    
    @property
    def ports(self):
        return self._ports
    
    @ports.setter
    def ports(self, value):
        self._ports.append(value)
    
    def run(self):
        yield self._process()
    

    def _process(self, **kwargs):
        return super()._process(**kwargs)
        