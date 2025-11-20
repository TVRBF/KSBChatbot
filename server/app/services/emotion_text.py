import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Use a widely-used DistilRoBERTa emotion model
MODEL_NAME = os.getenv("TEXT_EMOTION_MODEL", "j-hartmann/emotion-english-distilroberta-base")

# Load once at startup
_tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
_model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
_model.eval()

# Labels for the chosen model
LABELS = ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]

def detect_text_emotion(text: str):
    if not text.strip():
        return {"label": "neutral", "scores": {"neutral": 1.0}}

    inputs = _tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
    with torch.no_grad():
        outputs = _model(**inputs)
        scores = torch.softmax(outputs.logits, dim=-1).squeeze().tolist()

    # Map scores to labels
    result = {label: float(scores[i]) for i, label in enumerate(LABELS)}
    top_label = max(result, key=result.get)
    return {"label": top_label, "scores": result}
