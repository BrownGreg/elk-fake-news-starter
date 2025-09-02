import os
import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Dossier du modèle Hugging Face (celui que tu as montré)
# Ex: app/camembert_fakenews_model
MODEL_DIR = os.getenv("MODEL_DIR", "app/camembert_fakenews_model")

class HFSequenceClassifier:
    def __init__(self, model_dir: str):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_dir)
        self.model.to(self.device)
        self.model.eval()

        # Récupère les labels à partir de la config si dispo (id2label)
        id2label = getattr(self.model.config, "id2label", None)
        if id2label and isinstance(id2label, dict):
            # ordonne par id 0..N-1
            self.classes_ = np.array([id2label[str(i)] if str(i) in id2label else id2label[i] for i in range(self.model.config.num_labels)])
        else:
            # fallback générique
            self.classes_ = np.array([f"L{i}" for i in range(self.model.config.num_labels)])

    def predict_proba(self, texts):
        # batch tokenization
        enc = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt",
        )
        enc = {k: v.to(self.device) for k, v in enc.items()}
        with torch.no_grad():
            logits = self.model(**enc).logits
            probs = F.softmax(logits, dim=-1).cpu().numpy()
        return probs

def load_model():
    # charge ton modèle HF local
    return HFSequenceClassifier(MODEL_DIR)

def predict(model, text: str):
    proba = model.predict_proba([text])[0]
    print(f"Probabilités pour le texte : {text[:60]}... => {proba}")
    label_idx = int(np.argmax(proba))
    label = str(model.classes_[label_idx])
    score = float(proba[label_idx])
    return label, score
