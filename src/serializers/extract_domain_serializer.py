try:
    from urllib.parse import urlparse
except ImportError:
    print("No module named 'urllib' found")

from src.interfaces.domain_serializer import DomainSerializer

class ExtractUriSerializer(DomainSerializer):
    
    def serialize(self, uri: str=''):
        parsed_uri = urlparse(uri)
        return parsed_uri.netloc
