import os
import pytest
from elasticsearch import Elasticsearch

ES_HOST = os.getenv('ES_HOST', 'http://localhost:9200')
ES_USER = os.getenv('ES_USER', 'elastic')
ES_PASSWORD = os.getenv('ES_PASSWORD', 'changeme')

@pytest.mark.integration
def test_index_and_get_document():
    es = Elasticsearch(hosts=[ES_HOST], basic_auth=(ES_USER, ES_PASSWORD), verify_certs=False)
    assert es.ping(), 'Elasticsearch should be reachable'

    index_name = 'fake_news_test'
    doc = {'title': 'Test', 'text': 'Hello ES', 'pred_label': 'fake', 'pred_score': 0.99}

    res = es.index(index=index_name, document=doc)
    doc_id = res['_id']
    got = es.get(index=index_name, id=doc_id)
    assert got['_source']['title'] == 'Test'
