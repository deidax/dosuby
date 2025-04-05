import re
from dosuby.src.adapter.webserver_scanning.http_client_webserver_scanning_adapter import HttpClientWebserverScanningAdapter
from dosuby.src.interfaces.webserver_enumeration_adapter import WebserverEnumerationAdapter

class GenericWebServerScanningAdapter(WebserverEnumerationAdapter):
    """Generic adapter for any web server not covered by specialized adapters"""
    
    def __init__(self) -> None:
        super().__init__()
    
    def _process(self) -> dict:
        """
        Process generic server detection to handle servers not covered by other adapters
        
        Returns:
            dict: Detection information including server name, version if possible
        """
        try:
            # Use the base HTTP client method to get server header
            http_adapter = HttpClientWebserverScanningAdapter()
            http_adapter.target_uri = self.target_uri
            server_header = http_adapter.run()
            
            if not server_header or server_header == "Unknown" or server_header == "N/A":
                return {"detected": False}
            
            # Generic pattern for server/version
            server_pattern = r'^([a-zA-Z\-_]+)(?:/|\ )([\d\.]+)'
            match = re.search(server_pattern, server_header)
            
            if match:
                server = match.group(1)
                version = match.group(2)
                return {
                    "detected": True,
                    "server": server,
                    "version": version,
                    "confidence": "Medium",
                    "raw_header": server_header
                }
            else:
                # Try to get just the server name without version
                server_name_pattern = r'^([a-zA-Z\-_]+)'
                name_match = re.search(server_name_pattern, server_header)
                
                if name_match:
                    server = name_match.group(1)
                    return {
                        "detected": True,
                        "server": server,
                        "version": None,
                        "confidence": "Low",
                        "raw_header": server_header
                    }
                else:
                    # Return the raw header if we can't parse it
                    return {
                        "detected": True,
                        "server": server_header,
                        "version": None,
                        "confidence": "Low",
                        "raw_header": server_header
                    }
            
        except Exception as e:
            print(f"Error in generic server detection: {str(e)}")
            return {"detected": False}