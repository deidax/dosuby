from dosuby.src.serializers.extract_domain_serializer import ExtractUriSerializer



def test_serializer_value():
    
    ser_uri = ExtractUriSerializer.serialize(uri='domain.com')
    
    assert ser_uri == 'domain.com'