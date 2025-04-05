import re
from dosuby.src.adapter.webserver_scanning.http_client_webserver_scanning_adapter import HttpClientWebserverScanningAdapter
from dosuby.src.interfaces.webserver_enumeration_adapter import WebserverEnumerationAdapter

class NginxWebServerScanningAdapter(WebserverEnumerationAdapter):
    """Adapter for scanning Nginx web servers and detecting versions"""
    
    def __init__(self) -> None:
        super().__init__()
        self.server_name = "Nginx"
    
    def _process(self) -> dict:
        """
        Process Nginx server detection and version extraction
        
        Returns:
            dict: Detection information including server name, version, and confidence level
        """
        try:
            # Use the base HTTP client method to get server header
            http_adapter = HttpClientWebserverScanningAdapter()
            http_adapter.target_uri = self.target_uri
            server_header = http_adapter.run()
            
            if not server_header or server_header == "Unknown" or server_header == "N/A":
                return {"detected": False}
            
            # Nginx specific pattern
            nginx_pattern = r'nginx(?:/|\ )([\d\.]+)'
            match = re.search(nginx_pattern, server_header, re.IGNORECASE)
            
            if match:
                version = match.group(1)
                return {
                    "detected": True,
                    "server": "Nginx",
                    "version": version,
                    "confidence": "High",
                    "raw_header": server_header
                }
            elif "nginx" in server_header.lower():
                # Nginx is present but version not detected
                return {
                    "detected": True,
                    "server": "Nginx",
                    "version": None,
                    "confidence": "Medium",
                    "raw_header": server_header
                }
            
            return {"detected": False}
            
        except Exception as e:
            print(f"Error in Nginx detection: {str(e)}")
            return {"detected": False}