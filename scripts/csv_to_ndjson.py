import argparse
import pandas as pd
import json

def to_bulk_lines(df, index_name: str):
    for _, row in df.iterrows():
        meta = {'index': {'_index': index_name}}
        yield json.dumps(meta, ensure_ascii=False)
        doc = {
            'title': row.get('title', ''),
            'text': row.get('text', ''),
            'label': row.get('label', None)
        }
        yield json.dumps(doc, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description='Convert CSV to NDJSON for Elasticsearch _bulk API.')
    parser.add_argument('--csv', required=True, help='Path to input CSV file (expects columns: title,text,label).')
    parser.add_argument('--out', required=True, help='Output NDJSON file path.')
    parser.add_argument('--index', default='fake_news_raw', help='Target index name used in bulk meta lines.')
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    with open(args.out, 'w', encoding='utf-8') as w:
        for line in to_bulk_lines(df, args.index):
            w.write(line + '\n')

if __name__ == '__main__':
    main()
