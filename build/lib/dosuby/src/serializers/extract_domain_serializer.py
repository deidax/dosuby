try:
    from urllib.parse import urlparse
except ImportError:
    print("No module named 'urllib' found")

from dosuby.src.interfaces.domain_serializer import DomainSerializer

class ExtractUriSerializer(DomainSerializer):
    
    def serialize(uri: str=''):
        parsed_uri = urlparse(uri)
        parsed_uri = parsed_uri.netloc 
        if parsed_uri == '':
            return uri
        return parsed_uri
