import pytest
from src.adapter.dorks.google_dorks_adapter import GoogleDorksAdapter


def test_google_dorks_are_set_correctly():
    moke_queries = ['site:*.domain.com', 'inurl:domain.com']
    
    