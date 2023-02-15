try:
    import socket
except ImportError:
    print("No module named 'socket' found")
    
from src.interfaces.security_enumeration import SecurityEnumeration

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
        if kwargs.get('target_uri'):
            target_uri = kwargs.get('target_uri')
            for port in self.ports:
                result = self.engine.connect_ex(target_uri, port)
                yield result
            self.engine.close()
        else:
            raise ValueError('attribute is not supported')
        