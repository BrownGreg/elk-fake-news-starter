from app.model import load_model, predict

def test_predict_returns_label_and_score():
    model = load_model()
    label, score = predict(model, 'This is a sample news text.')
    assert label in ['fake', 'real']
    assert 0.0 <= float(score) <= 1.0
