import pytest
from dosuby.src.adapter.dorks.google_dorks_adapter import GoogleDorksAdapter
import unittest.mock


def test_google_dorks_are_set_correctly(monkeypatch):
    
    target_uri = 'faketarget.com'
    
    moke_queries = [f'site:*.{target_uri}', f'inurl:{target_uri}']
    
    monkeypatch.setattr(GoogleDorksAdapter, 'queries', moke_queries)
    
    google_dork = GoogleDorksAdapter()
    
    assert google_dork.queries == ['site:*.faketarget.com', 'inurl:faketarget.com']

def test_add_a_new_google_dork_query(monkeypatch):
    
    target_uri = 'faketarget.com'
    
    moke_queries = [f'site:*.{target_uri}', f'inurl:{target_uri}']
    
    monkeypatch.setattr(GoogleDorksAdapter, 'queries', moke_queries)
    
    google_dork = GoogleDorksAdapter()
    
    google_dork.add_dork_queries(query=f'{target_uri} test_query')
    
    assert google_dork.queries == ['site:*.faketarget.com', 'inurl:faketarget.com', 'faketarget.com test_query']
    