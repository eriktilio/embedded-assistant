from sentence_transformers import SentenceTransformer, util
from .intents import INTENTS
from ..core.logger import log

model = SentenceTransformer("all-MiniLM-L6-v2")

INTENT_NAMES = list(INTENTS.keys())
INTENT_TEXTS = list(INTENTS.values())

intent_embeddings = model.encode(INTENT_TEXTS, convert_to_tensor=True)


def detect_intent(text: str, threshold: float = 0.45) -> dict:
    text_embedding = model.encode(text, convert_to_tensor=True)

    scores = util.cos_sim(text_embedding, intent_embeddings)[0]

    best_idx = scores.argmax().item()
    confidence = float(scores[best_idx].item())
    intent = INTENT_NAMES[best_idx]

    log("NLP", f"{intent} ({confidence:.2f}) | input='{text}'")

    if confidence < threshold:
        return {
            "intent": "fallback",
            "confidence": confidence,
            "source": "nlp"
        }

    return {
        "intent": intent,
        "confidence": confidence,
        "source": "nlp"
    }