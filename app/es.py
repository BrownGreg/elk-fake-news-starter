
from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv

def get_es() -> Elasticsearch:
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
    host = os.getenv('ES_HOST', 'http://localhost:9200')
    user = os.getenv('ES_USER', 'elastic')
    password = os.getenv('ES_PASSWORD', 'changeme')
    return Elasticsearch(hosts=[host], basic_auth=(user, password), verify_certs=False)
