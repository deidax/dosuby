try:
    from socket import *
except ImportError:
    print("SocketPortScanningAdapter: No module named 'socket' found")

try:
    from threading import *
except ImportError:
    print("SocketPortScanningAdapter: No module named 'threading' found")

    
from dosuby.src.interfaces.ports_enumeration_adapter import PortEnumerationAdapter

class SocketPortScanningAdapter(PortEnumerationAdapter):
    
    def __init__(self) -> None:
        """This class will manage the port enumeration logic using Sockets

        """
        super().__init__()
        
    
    
    def _process(self, ip, port):
        try:
            # creates a socket object to connect to that port on the target host.
            server_sock = socket(AF_INET, SOCK_STREAM)
            server_sock.settimeout(1.5)
            # If the connection is successful, the method yields the open port number.
            result = server_sock.connect((ip, port))
            yield port
        except:
            # If there's no connection return nothing
            return
        finally:
            # close socket connection
            server_sock.close()
    
    def _scan(self, ip):
    # The _scan method iterates through the range of ports to scan 
    # and calls the _process method on each port.
    # If an open port is found, it yields the open port number.
        for port in self.ports:
            for open_port in self._process(ip, port):
                yield open_port
    
    def run(self):
        # get ip of target domain
        target_ip = gethostbyname(self.target_uri)
        # Create an empty list to store the threads
        threads = []
        # Loop through the range of ports to scan
        for port in self.ports:
            # Create a new thread for each port
            thread = Thread(target=self._process, args=(target_ip, port))
            # Add the thread to the list
            threads.append(thread)
            # Start the thread
            thread.start()
        
        # Wait for all threads to finish
        for thread in threads:
            thread.join()
        
        open_ports = list(self._scan(target_ip))
        return open_ports
    


    
