import pytest
from dosuby.src.interfaces.success_response import SuccessResponse
from dosuby.src.core.domain.target import Target
from dosuby.src.serializers.extract_domain_serializer import ExtractUriSerializer



# def test_success_response_has_global_final_result():
    
#     target_1 = Target(target_uri='domain.com', subdomain_serializer=ExtractUriSerializer)
#     success_response_1 = SuccessResponse()
#     success_response_1.set_target(target=target_1)
    
#     success_response_1.target.add_subdomain('sub1.domain.com')
#     success_response_1.target.add_subdomain('sub2.domain.com')
    
    
#     target_2 = Target(target_uri='domain.com', subdomain_serializer=ExtractUriSerializer)
#     success_response_2 = SuccessResponse()
#     success_response_2.set_target(target=target_2)
    
#     success_response_2.target.add_subdomain('sub3.domain.com')
#     success_response_2.target.add_subdomain('sub4.domain.com')
    
#     subdomains = success_response_2.get_target_subdomains()
    
    
#     assert target_1 is target_2
    
#     assert subdomains == ['sub1.domain.com','sub2.domain.com','sub3.domain.com','sub4.domain.com']