import pytest
from src.core.domain.target import Target

def test_init_target():
    target = Target()
    
    assert target.subdomains == []

def test_add_subdomain():
    target = Target()
    target_subdomains_1 = 'test1.domain.com'
    target_subdomains_2 = 'test2.domain.com'
    
    target.add_subdomain(subdomain=target_subdomains_1)
    target.add_subdomain(subdomain=target_subdomains_2)
    
    assert target.subdomains == ['test1.domain.com', 'test2.domain.com']