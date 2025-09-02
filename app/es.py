from elasticsearch import Elasticsearch
import os

def get_es() -> Elasticsearch:
    host = os.getenv('ES_HOST', 'http://localhost:9200')
    user = os.getenv('ES_USER', 'elastic')
    password = os.getenv('ES_PASSWORD', 'changeme')
    return Elasticsearch(hosts=[host], basic_auth=(user, password), verify_certs=False)
