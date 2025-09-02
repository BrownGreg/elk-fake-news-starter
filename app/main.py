from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timezone
from .model import load_model, predict
from .es import get_es


app = FastAPI(title='Fake News Classifier API', version='1.0.0')

model = load_model()
es = get_es()

class News(BaseModel):
    title: str
    text: str

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.post('/classify')
def classify(news: News):
    label, score = predict(model, news.text)
    doc = {
        'title': news.title,
        'text': news.text,
        'pred_label': label,
        'pred_score': float(score),
        'created_at': datetime.now(timezone.utc).isoformat()
    }
    res = es.index(index='fake_news', document=doc)
    return {'indexed_id': res.get('_id'), 'label': label, 'score': score, 'doc': doc}
