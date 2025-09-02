import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib

def main():
    parser = argparse.ArgumentParser(description='Train a baseline text classifier and save model.pkl')
    parser.add_argument('--csv', required=True, help='CSV with columns: title,text,label')
    parser.add_argument('--out', default='model.pkl', help='Output model path')
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    df = df.dropna(subset=['text', 'label'])

    X = df['text'].astype(str).values
    y = df['label'].astype(str).values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    pipe = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=30000, ngram_range=(1,2))),
        ('clf', LogisticRegression(max_iter=200))
    ])

    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    print(classification_report(y_test, y_pred))

    joblib.dump(pipe, args.out)
    print(f'Saved model to {args.out}')

if __name__ == '__main__':
    main()
