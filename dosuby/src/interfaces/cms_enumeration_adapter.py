from dosuby.src.interfaces.security_enumeration import SecurityEnumeration
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CMSEnumerationAdapter(SecurityEnumeration):
    
    def __init__(self) -> None:
        """Base class for CMS enumeration adapters
        
        This class provides common functionality for detecting CMS systems
        and their versions across subdomains.
        """
        super().__init__()
        self.subdomain_uri = ''
        self.user_agent = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
        }
        self.timeout = 10  # Add a timeout for requests
        
    def run(self):
        """Run the CMS detection process"""
        if not self.subdomain_uri:
            return None
        return self._process(uri=self.subdomain_uri)
    
    def _process(self, **kwargs):
        """Process the CMS detection and version identification"""
        return super()._process(**kwargs)
    
    def make_request(self, uri, path, allow_redirects=False):
        """Make an HTTP request to the specified URI and path
        
        Args:
            uri (str): The subdomain URI
            path (str): The path to request
            allow_redirects (bool): Whether to follow redirects
            
        Returns:
            requests.Response: The HTTP response
        """
        try:
            return requests.get(
                f"http://{uri}{path}", 
                allow_redirects=allow_redirects, 
                headers=self.user_agent, 
                verify=False,
                timeout=self.timeout
            )
        except requests.RequestException:
            # Create a dummy response object for failed requests
            response = requests.Response()
            response.status_code = 0
            return response
            
    def detect_cms(self):
        """Detect if a CMS is present
        
        Returns:
            dict: CMS detection result with type and confidence level
        """
        raise NotImplementedError("detect_cms is not implemented")
        
    def detect_version(self):
        """Detect the version of the CMS if present
        
        Returns:
            str: Version string if detected, None otherwise
        """
        raise NotImplementedError("detect_version is not implemented")
        
    def get_result(self):
        """Get the final detection result
        
        Returns:
            dict: Detection result including CMS type, version, and confidence
        """
        cms_info = self.detect_cms()
        if cms_info and cms_info.get('detected'):
            version = self.detect_version()
            cms_info['version'] = version
            return cms_info
        return None