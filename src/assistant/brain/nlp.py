import pickle
from pathlib import Path
from ..core.logger import log


BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "brain"


with open(MODEL_DIR / "vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open(MODEL_DIR / "intent_model.pkl", "rb") as f:
    model = pickle.load(f)


def detect_intent(text: str) -> dict:
    X = vectorizer.transform([text])

    intent = model.predict(X)[0]

    probs = model.predict_proba(X)[0]
    confidence = float(max(probs))

    log("NLP", f"{intent} ({confidence:.2f}) | input='{text}'")

    if confidence < 0.45:
        return {"intent": "fallback", "confidence": confidence, "source": "nlp"}

    return {"intent": intent, "confidence": confidence, "source": "nlp"}
