# ELK + FastAPI Fake News – Starter Kit

This repo is a ready-to-use scaffold to complete your TP.

## 0) Prerequisites
- Docker & Docker Compose
- Python 3.9+
- Git, curl or HTTPie/Postman
- A CSV dataset with columns: `title,text,label`
- Your packaged model (`model.pkl`) **or** use the optional baseline trainer

## 1) Launch docker-elk
```bash
git clone https://github.com/deviantony/docker-elk
cd docker-elk
# If needed: cp .env.example .env and set passwords
docker compose up -d
docker compose ps
# Wait until Kibana is up at http://localhost:5601  (user: elastic / pass: changeme by default)
```

## 2) Minimal security
In Kibana → **Dev Tools**:
- Change default password if needed (see docker-elk docs)
- Create a role with read/write on `fake_news*` and an `api_app` user bound to that role

## 3) Index template, index, alias
Open `kibana/dev_tools_snippets.http` and paste in Kibana Console:
- Create index template
- Create `fake_news_v1`
- Create `fake_news` alias

## 4) Import CSV
**Option A – Kibana UI**: ML → Data Visualizer → Import file → target index `fake_news_raw`  
**Option B – Bulk API**:
```bash
# Convert CSV to NDJSON
python scripts/csv_to_ndjson.py --csv /path/to/fake_news.csv --out /tmp/fake_news.ndjson --index fake_news_raw

# Post to _bulk
make bulk IN=/tmp/fake_news.ndjson HOST=http://localhost:9200 USER=elastic PASS=changeme
# or:
# curl -H "Content-Type: application/x-ndjson" -u elastic:changeme -XPOST localhost:9200/_bulk --data-binary @/tmp/fake_news.ndjson
```

## 5) FastAPI service
```bash
cp .env.example .env  # then edit ES_HOST/ES_USER/ES_PASSWORD if needed
python -m venv .venv && . .venv/bin/activate
pip install -r app/requirements.txt
uvicorn app.main:app --reload --port 8000
```

Test:
```bash
curl -X POST http://localhost:8000/classify -H "Content-Type: application/json" \
  -d '{"title":"Exemple","text":"Contenu de la news"}'
```

Verify in Kibana Dev Tools:
```http
GET fake_news/_search
{
  "sort": [{ "created_at": "desc" }],
  "size": 5
}
```

### Using your own model
Put `model.pkl` at project root (or set `MODEL_PATH` env var) and restart the API.

Optional baseline trainer:
```bash
python scripts/train_baseline.py --csv /path/to/fake_news.csv --out model.pkl
```

## 6) Kibana dashboard
1. Create a **Data View** on alias `fake_news`
2. Discover → inspect incoming docs
3. Visualizations to include:
   - Histogram of `pred_label` per day (Date histogram on `created_at`, split by `pred_label`)
   - Metric: percentage of `pred_label == "fake"`
   - Heatmap: `pred_score` by hour of day vs day of week
4. Assemble in a dashboard named **Fake News Monitoring** and **export** it (Management → Saved Objects) as NDJSON

## 7) Direct ES insert (no FastAPI) – quick path
From a notebook/script:
```http
POST fake_news/_doc
{ "title":"...", "text":"...", "pred_label":"fake", "pred_score":0.82, "created_at":"2025-01-01T00:00:00Z" }
```

## 8) Tests & automation
```bash
pytest -q                 # unit tests
pytest -m integration -q  # requires ES up locally
```
Makefile provides `install`, `run`, `test`, and a `bulk` helper.

## 9) Bonus ideas
- Put the FastAPI service into Docker + docker compose
- Add an ingest pipeline (HTML cleanup, language detection)
- Add Watcher/Alert (email when fake ratio exceeds threshold)
- Token-based auth on FastAPI
- Dedicated index for API logs
- Try OpenSearch Dashboard too

## Deliverables
1. 2-page report with architecture, key steps, dashboard screenshots, difficulties & solutions
2. Source code + `requirements.txt`
3. NDJSON file if you used Bulk
4. Kibana dashboard export (.ndjson)
