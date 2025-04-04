try:
    import http.client
except ImportError:
    print("HttpClientWebserverScanning: No module named 'http' found")

    
from dosuby.src.interfaces.webserver_enumeration_adapter import WebserverEnumerationAdapter

class HttpClientWebserverScanningAdapter(WebserverEnumerationAdapter):
    
    def __init__(self) -> None:
        """This class will manage the port enumeration logic using Sockets

        """
        super().__init__()
    
    
    def _process(self) -> str:
        conn = http.client.HTTPConnection(self.target_uri)
        conn.request("GET", "/")
        response = conn.getresponse()
        server_header = response.getheader("Server")
        if server_header:
            return server_header
        else:
            return "Unknown"
        



    
