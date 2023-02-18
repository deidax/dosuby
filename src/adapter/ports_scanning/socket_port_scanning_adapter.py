try:
    from socket import *
except ImportError:
    print("SocketPortScanningAdapter: No module named 'socket' found")

try:
    from threading import *
except ImportError:
    print("SocketPortScanningAdapter: No module named 'threading' found")

    
from src.interfaces.ports_enumeration_adapter import PortEnumerationAdapter

class SocketPortScanningAdapter(PortEnumerationAdapter):
    
    def __init__(self) -> None:
        """This class will manage the port enumeration logic using the Sockets

        """
        super().__init__()
        self.engine = socket(AF_INET, SOCK_STREAM)
    
    
    def run(self):
        ip_address = gethostbyname(self.target_uri)
        for port in self.ports:
            t = Thread(target=self._process, args=(ip_address, port))
            t.start()
    

    def _process(self, ip, port):
        # try:
        #     print('[+] -->'.format(ip))
        #     self.engine.settimeout(5)
        #     result = self.engine.connect((ip, port))
        #     print('[+] {}/tcp open'.format(port))
        # except:
        #     return
        # finally:
        #     self.engine.close()
        print("Thread started")
        print('---->')
        print("Thread finished")
    