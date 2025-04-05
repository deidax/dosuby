import re
from dosuby.src.adapter.webserver_scanning.http_client_webserver_scanning_adapter import HttpClientWebserverScanningAdapter
from dosuby.src.interfaces.webserver_enumeration_adapter import WebserverEnumerationAdapter

class LighttpdWebServerScanningAdapter(WebserverEnumerationAdapter):
    """Adapter for scanning Lighttpd web servers and detecting versions"""
    
    def __init__(self) -> None:
        super().__init__()
        self.server_name = "Lighttpd"
    
    def _process(self) -> dict:
        """
        Process Lighttpd server detection and version extraction
        
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
            
            # Lighttpd specific pattern
            lighttpd_pattern = r'lighttpd(?:/|\ )([\d\.]+)'
            match = re.search(lighttpd_pattern, server_header, re.IGNORECASE)
            
            if match:
                version = match.group(1)
                return {
                    "detected": True,
                    "server": "Lighttpd",
                    "version": version,
                    "confidence": "High",
                    "raw_header": server_header
                }
            elif "lighttpd" in server_header.lower():
                # Lighttpd is present but version not detected
                return {
                    "detected": True,
                    "server": "Lighttpd",
                    "version": None,
                    "confidence": "Medium",
                    "raw_header": server_header
                }
            
            return {"detected": False}
            
        except Exception as e:
            print(f"Error in Lighttpd detection: {str(e)}")
            return {"detected": False}