.PHONY: install run test bulk

install:
	python -m venv .venv && . .venv/bin/activate && pip install -r app/requirements.txt

run:
	. .venv/bin/activate && uvicorn app.main:app --reload --port 8000

test:
	. .venv/bin/activate && pytest -q

# Example: make bulk IN=./data/fake_news.ndjson HOST=http://localhost:9200 USER=elastic PASS=changeme
bulk:
	curl -s -H "Content-Type: application/x-ndjson" -u $${USER}:$${PASS} -XPOST $${HOST}/_bulk --data-binary @$${IN} | jq .errors
