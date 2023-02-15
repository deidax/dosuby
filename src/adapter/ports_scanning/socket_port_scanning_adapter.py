try:
    import socket
except ImportError:
    print("No module named 'socket' found")
    
from src.interfaces.security_enumeration import SecurityEnumeration
from src.core.domain.target import Target

class SocketPortScanningAdapter(SecurityEnumeration):
    
    def __init__(self) -> None:
        """This class will manage the port enumeration logic using the Sockets

        """
        super().__init__()
        self._ports = []
        self.engine = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    @property
    def ports(self):
        return self._ports
    
    @ports.setter
    def ports(self, value):
        self._ports.append(value)
    

    def _process(self, **kwargs):
        if kwargs.get('target'):
            target = kwargs.get('target')
            if isinstance(target, Target):
                for port in self.ports:
                    result = self.engine.connect_ex(target.target_uri, port)
                    yield result
                self.engine.close()
            else:
                raise ValueError('target must be a Instance of Target')
        