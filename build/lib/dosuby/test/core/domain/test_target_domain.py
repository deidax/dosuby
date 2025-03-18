import pytest
from dosuby.src.core.domain.target import Target
from dosuby.src.serializers.extract_domain_serializer import ExtractUriSerializer

# def test_init_target():
#     target = Target(target_uri='domain.test.com')
    
#     assert target.subdomains == []


# def test_if_target_is_a_singleton():
    
#     target_1 = Target(target_uri='domain.com')
#     target_2 = Target(target_uri='domain.com')
    
#     assert target_1 is target_2


# def test_add_subdomain():
#     target = Target(target_uri='domain.com', subdomain_serializer=ExtractUriSerializer)
#     target_subdomains_1 = 'test1.domain.com'
#     target_subdomains_2 = 'test2.domain.com'
    
#     target.add_subdomain(subdomain=target_subdomains_1)
#     target.add_subdomain(subdomain=target_subdomains_2)
    
#     assert target.subdomains == ['test1.domain.com', 'test2.domain.com']

# def test_adding_a_duplicated_subdomain():
#     target = Target(target_uri='domain.com')
#     target_subdomains_1 = 'test1.domain.com'
#     target_subdomains_2 = 'test2.domain.com'
    
#     target.add_subdomain(subdomain=target_subdomains_1)
#     target.add_subdomain(subdomain=target_subdomains_2)
    
#     assert target.add_subdomain(subdomain=target_subdomains_2) is False

# def test_adding_a_new_subdomain():
#     target = Target(target_uri='domain.com')
#     target_subdomains_1 = 'test1.domain.com'
#     target_subdomains_2 = 'test2.domain.com'
#     target_subdomains_3 = 'test3.domain.com'
    
#     target.add_subdomain(subdomain=target_subdomains_1)
#     target.add_subdomain(subdomain=target_subdomains_2)
    
#     assert target.add_subdomain(subdomain=target_subdomains_3) is True


# def test_check_if_result_is_accurate():
#     target = Target(target_uri='domain.com')
#     target_subdomains_1 = 'test1.domain.com'
#     target_subdomains_2 = 'test2.domainn.com'
#     target_subdomains_3 = 'test3.domain.com'
    
#     target.add_subdomain(subdomain=target_subdomains_1)
#     target.add_subdomain(subdomain=target_subdomains_2)
#     target.add_subdomain(subdomain=target_subdomains_3)
    
#     subdomains = target.subdomains
    
#     assert  len(subdomains) == 2
    

